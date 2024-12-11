<template>
  <div class="mx-5">
    <canvas ref="myCanvas" width="450" height="750" style="border: 1px solid grey"></canvas>
  </div>
</template>
<script>
import { FetchAPI } from '@/utils/apiRequest'

export default {
  name: 'CanvasDisplay',
  data() {
    return {
      processData: [],
    }
  },
  mounted() {
    this.fetchImage()
    this.fetchData()
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
     * Fetch the process data from the database
     */
    async fetchData() {
      const fetchApi = new FetchAPI()
      const res = await fetchApi.get('/api/process')
      for (const data of res.data) {
        const obj = {
          id: data.id,
          x: data.x_coord,
          y: data.y_coord,
          width: data.width,
          height: data.height,
          productNum: data.product_num,
        }
        this.processData.push(obj)
      }
    },

    /**
     * Function to generate the Canvas using the image url as parameter
     * @param {String} imageDB - the image url from the database
     */

    generateCanvas(imageDB) {
      const canvas = this.$refs.myCanvas
      const ctx = canvas.getContext('2d')
      const image = new Image()
      image.src = imageDB

      const styleLabel = (ctx, x, y, radius, label, fillStyle, strokeStyle) => {
        ctx.beginPath()
        ctx.arc(x, y, radius, 0, Math.PI * 2)
        ctx.closePath()
        ctx.fillStyle = fillStyle
        ctx.fill()
        ctx.strokeStyle = strokeStyle
        ctx.lineWidth = 3
        ctx.stroke()

        ctx.font = 'bold 15px Arial'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillStyle = 'white'
        ctx.fillText(label, x, y)
      }
      // Load image with the process boxes
      image.onload = () => {
        // Draw the image on the canvas
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height)

        // Loop through the data and draw each rectangle
        this.processData.forEach((rect) => {
          // Draw the rectangle
          ctx.fillStyle = this.setColor(rect.productNum)
          ctx.strokeStyle = ''
          ctx.strokeStyle = 'white'
          ctx.strokeRect(rect.x, rect.y, rect.width, rect.height)
          ctx.fillRect(rect.x, rect.y, rect.width, rect.height)

          // Draw label inside a circle
          const circleX = rect.x + rect.width / 2
          const circleY = rect.y + rect.height / 2
          styleLabel(ctx, circleX, circleY, 15, rect.id, 'transparent', 'white')
        })
      }
    },

    /**
     * Function to set the color of canvas based on their productNum
     * @param {Number} status - parameter for the productNum of the canvas
     */

    setColor(status) {
      if (status === 1) {
        return 'green'
      } else if (status === 2) {
        return 'red'
      }
    },
  },
}
</script>
