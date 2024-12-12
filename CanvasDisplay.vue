<template>
  <div class="mx-5">
    <canvas ref="myCanvas"></canvas>
  </div>
</template>
<script>
import { FetchAPI } from '@/utils/apiRequest'

export default {
  name: 'CanvasDisplay',
  props: {
    processArray: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      ctx: null,
      canvas: null,
    }
  },
  mounted() {
    this.fetchImage()
  },
  methods: {
    /**
     * Function to get the image from backend
     */

    async fetchImage() {
      const fetchApi = new FetchAPI()
      try {
        const response = await fetchApi.get('/api/yellow-line/image/lane.png', {
          responseType: 'blob',
        })
        const imageURL = URL.createObjectURL(response)
        this.generateCanvas(imageURL)
      } catch (error) {
        console.error('Error fetching the image:', error)
      }
    },

    /**
     * Initialize canvas context
     */
    initiateCanvas() {
      this.canvas = this.$refs.myCanvas
      this.ctx = this.canvas.getContext('2d')
      this.canvas.width = 450
      this.canvas.height = 750
    },

    /**
     * Function to generate the Canvas using the image url as parameter
     * @param {String} imageDB - the image url from the database
     */
    generateCanvas(imageDB) {
      this.initiateCanvas()
      const image = new Image()
      image.src = imageDB

      // Load image with the process boxes
      image.onload = () => {
        // Draw the image on the canvas
        this.ctx.drawImage(image, 0, 0, this.canvas.width, this.canvas.height)

        // Loop through the data and draw each rectangle
        this.processArray.forEach((rect) => {
          const { fillStyle, strokeStyle, textColor } = this.setColor(rect.productNum)
          // Draw the rectangle
          this.ctx.fillStyle = fillStyle
          this.ctx.fillRect(rect.x, rect.y, rect.width, rect.height)
          this.ctx.strokeStyle = 'white'
          this.ctx.lineWidth = 2
          this.ctx.strokeRect(rect.x, rect.y, rect.width, rect.height)

          // Draw label inside a circle
          const circleX = rect.x + rect.width / 2
          const circleY = rect.y + rect.height / 2
          this.styleLabel(circleX, circleY, 15, rect.id, fillStyle, strokeStyle, textColor)
        })
      }
    },

    /**
     * Style the label displayed in boxes
     * @param {Number} x - x coordinate
     * @param {Number} y - y coordinate
     * @param {Number} radius - radius of circle
     * @param {String} label - text to be displayed
     * @param {String} fillStyle - background color of the circle
     * @param {String} strokeStyle - color of the border line
     * @param {String} textColor - color of the text
     */
    styleLabel(x, y, radius, label, fillStyle, strokeStyle, textColor) {
      this.ctx.beginPath()
      this.ctx.arc(x, y, radius, 0, Math.PI * 2)
      this.ctx.closePath()
      this.ctx.fillStyle = fillStyle
      this.ctx.fill()
      this.ctx.strokeStyle = strokeStyle
      this.ctx.lineWidth = 3
      this.ctx.stroke()

      this.ctx.font = 'bold 15px Arial'
      this.ctx.textAlign = 'center'
      this.ctx.textBaseline = 'middle'
      this.ctx.fillStyle = textColor
      this.ctx.fillText(label, x, y)
    },

    /**
     * Function to set the color of canvas based on their productNum
     * @param {Number} status - parameter for the productNum of the canvas
     */
    setColor(status) {
      const lookup = {
        1: {
          fillStyle: 'green',
          strokeStyle: 'white',
          textColor: 'white',
        },
        2: {
          fillStyle: 'red',
          strokeStyle: 'white',
          textColor: 'white',
        },
        3: {
          fillStyle: 'yellow',
          strokeStyle: 'black',
          textColor: 'black',
        },
      }

      return lookup[status]
    },
  },
}
</script>

<style scoped>
canvas {
  border: 1px solid grey;
}
</style>


// CanvasDisplay.spec.js

import { shallowMount } from '@vue/test-utils'
import CanvasDisplay from '@/components/CanvasDisplay.vue'
import { FetchAPI } from '@/utils/apiRequest'

jest.mock('@/utils/apiRequest', () => ({
  FetchAPI: jest.fn().mockImplementation(() => ({
    get: jest.fn(),
  })),
}))

describe('CanvasDisplay.vue', () => {
  let wrapper
  let fetchApiMock

  beforeEach(() => {
    fetchApiMock = new FetchAPI()
    wrapper = shallowMount(CanvasDisplay, {
      mocks: {
        $refs: {
          myCanvas: document.createElement('canvas'),
        },
      },
    })
  })

  afterEach(() => {
    jest.clearAllMocks()
    wrapper.unmount()
  })

  it('should call fetchImage and fetchData on mount', () => {
    const fetchImageSpy = jest.spyOn(wrapper.vm, 'fetchImage')
    const fetchDataSpy = jest.spyOn(wrapper.vm, 'fetchData')

    wrapper.vm.$options.mounted[0].call(wrapper.vm) // Call the mounted hook

    expect(fetchImageSpy).toHaveBeenCalled()
    expect(fetchDataSpy).toHaveBeenCalled()
  })

  it('should call fetchAPI and generateCanvas when fetchImage is successful', async () => {
    const mockBlob = new Blob(['image data'], { type: 'image/png' })
    const mockObjectURL = 'blob:http://localhost/image'

    global.URL.createObjectURL = jest.fn(() => mockObjectURL)
    fetchApiMock.get.mockResolvedValueOnce(mockBlob)

    await wrapper.vm.fetchImage()

    expect(fetchApiMock.get).toHaveBeenCalledWith('/api/yellow-line/image/lane.png', { responseType: 'blob' })
    expect(global.URL.createObjectURL).toHaveBeenCalledWith(mockBlob)
    expect(wrapper.vm.generateCanvas).toHaveBeenCalledWith(mockObjectURL)
  })

  it('should log an error if fetchImage fails', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
    const mockError = new Error('Fetch failed')
    fetchApiMock.get.mockRejectedValueOnce(mockError)

    await wrapper.vm.fetchImage()

    expect(consoleErrorSpy).toHaveBeenCalledWith('Error fetching the image:', mockError)

    consoleErrorSpy.mockRestore()
  })

  it('should call fetchAPI and update processData when fetchData is successful', async () => {
    const mockResponse = {
      data: [
        { id: 1, x_coord: 10, y_coord: 20, width: 50, height: 60, product_num: 1 },
        { id: 2, x_coord: 30, y_coord: 40, width: 70, height: 80, product_num: 2 },
      ],
    }
    fetchApiMock.get.mockResolvedValueOnce(mockResponse)

    await wrapper.vm.fetchData()

    expect(fetchApiMock.get).toHaveBeenCalledWith('/api/process')
    expect(wrapper.vm.processData).toEqual([
      { id: 1, x: 10, y: 20, width: 50, height: 60, productNum: 1 },
      { id: 2, x: 30, y: 40, width: 70, height: 80, productNum: 2 },
    ])
  })

  it('should call setColor correctly based on productNum', () => {
    expect(wrapper.vm.setColor(1)).toBe('green')
    expect(wrapper.vm.setColor(2)).toBe('red')
    expect(wrapper.vm.setColor(3)).toBeUndefined() // Default case
  })

  it('should draw image and process rectangles on the canvas when image is loaded', () => {
    const mockCtx = {
      drawImage: jest.fn(),
      beginPath: jest.fn(),
      arc: jest.fn(),
      closePath: jest.fn(),
      fill: jest.fn(),
      stroke: jest.fn(),
      fillRect: jest.fn(),
      strokeRect: jest.fn(),
      font: '',
      textAlign: '',
      textBaseline: '',
      fillStyle: '',
      strokeStyle: '',
      lineWidth: 0,
      fillText: jest.fn(),
    }

    const canvas = wrapper.vm.$refs.myCanvas
    const mockImage = new Image()
    jest.spyOn(canvas, 'getContext').mockReturnValue(mockCtx)
    wrapper.vm.processData = [
      { id: 1, x: 10, y: 20, width: 50, height: 60, productNum: 1 },
    ]

    wrapper.vm.generateCanvas('mockImageUrl')
    mockImage.onload()

    expect(mockCtx.drawImage).toHaveBeenCalledWith(mockImage, 0, 0, canvas.width, canvas.height)
    expect(mockCtx.fillRect).toHaveBeenCalledWith(10, 20, 50, 60)
    expect(mockCtx.strokeRect).toHaveBeenCalledWith(10, 20, 50, 60)
    expect(mockCtx.fillText).toHaveBeenCalledWith('1', 35, 50)
  })

  it('should style labels correctly on the canvas', () => {
    const mockCtx = {
      beginPath: jest.fn(),
      arc: jest.fn(),
      closePath: jest.fn(),
      fill: jest.fn(),
      stroke: jest.fn(),
      font: '',
      textAlign: '',
      textBaseline: '',
      fillStyle: '',
      strokeStyle: '',
      lineWidth: 0,
      fillText: jest.fn(),
    }

    const styleLabel = wrapper.vm.generateCanvas.toString().match(/styleLabel\(.*?\) {/)[0]
    expect(styleLabel).toBeTruthy()

    const x = 100, y = 150, radius = 15, label = '1', fillStyle = 'transparent', strokeStyle = 'white'

    eval(`(${styleLabel})(mockCtx, x, y, radius, label, fillStyle, strokeStyle)`)

    expect(mockCtx.beginPath).toHaveBeenCalled()
    expect(mockCtx.arc).toHaveBeenCalledWith(x, y, radius, 0, Math.PI * 2)
    expect(mockCtx.closePath).toHaveBeenCalled()
    expect(mockCtx.fillStyle).toBe(fillStyle)
    expect(mockCtx.fill).toHaveBeenCalled()
    expect(mockCtx.strokeStyle).toBe(strokeStyle)
    expect(mockCtx.lineWidth).toBe(3)
    expect(mockCtx.stroke).toHaveBeenCalled()
    expect(mockCtx.fillText).toHaveBeenCalledWith(label, x, y)
  })
})

