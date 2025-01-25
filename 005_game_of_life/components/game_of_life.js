export default {
    template: "<canvas></canvas>",
    props: {
        speed: Number,
        playing: Boolean,
        generation_num: Number,
    },
    mounted() {
        this.container = document.getElementById("c2")
        this.ctx = this.$el.getContext("2d");

        // Add event listeners
        window.onresize = this.update;
    },
    methods: {
        draw() {
            this.ctx.beginPath();
            this.ctx.moveTo(0, 0);
            this.ctx.lineTo(this.$el.width, this.$el.height);
            this.ctx.stroke();
        },
        update() {
            const width = this.container.offsetWidth;
            const height = this.container.offsetHeight;
            console.log(width, height)
            this.$el.width = width;
            this.$el.height = height;

            this.draw()
        },
    },
};
