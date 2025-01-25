export default {
    template: "<svg></svg>",
    props: {
        speed: Number,
        playing: Boolean,
        generation_num: Number,
        drawing: String,
    },
    mounted() {
        const svg = this.$el;
        this.container = document.getElementById("c2")

        // Add event listeners
        window.onresize = this.update;
    },
    methods: {
        update() {
            const gridWidth = this.container.offsetWidth;
            const gridHeight = this.container.offsetHeight;

            // Clear content
            const svg = this.$el;
            svg.innerHTML = "";

            // Configurations
            const squareSize = 16; // Size of each square in pixels
            const numColumns = Math.floor(gridWidth / squareSize) + 1;
            const numRows = Math.floor(gridHeight / squareSize) + 1;

            // Set SVG dimensions
            svg.setAttribute('width', gridWidth);
            svg.setAttribute('height', gridHeight);

            // Generate grid of squares
            for (let y = 0; y < numRows; y++) {
                for (let x = 0; x < numColumns; x++) {
                    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                    rect.setAttribute('x', `${x * squareSize}`);
                    rect.setAttribute('y', `${y * squareSize}`);
                    rect.setAttribute('width', `${squareSize}`);
                    rect.setAttribute('height', `${squareSize}`);
                    rect.setAttribute('fill', '#ffffff');
                    rect.setAttribute('stroke', '#bbb');
                    rect.setAttribute('stroke-width', '1');
                    svg.appendChild(rect);
                }
            }
            console.log(numColumns * numRows)
        },
    },
};
