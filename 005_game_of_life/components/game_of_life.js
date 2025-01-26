import {loadResource} from "../../static/utils/resources.js";


export default {
    template: "<div></div>",
    props: {
        resource_path: String,
        speed: Number,
        playing: Boolean,
        drawing: String,
    },
    async mounted() {
        await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
        await loadResource(window.path_prefix + `${this.resource_path}/p5/p5.min.js`);

        this.generation_num = 0;
        this.grid = [];
        this.size = 16;
        this.cols = 0;
        this.rows = 0;

        this.sketch = new p5((sketch) => {
            sketch.setup = function () {
                sketch.createCanvas(sketch.windowWidth, sketch.windowHeight);
            };
            // 60 FPS
            sketch.draw = this.draw;
        }, this.$el);

        // Add event listeners
        window.onresize = this.resize;
        window.onload = this.resize;
    },
    methods: {
        get_size() {
            return {
                width: this.sketch.windowWidth,
                height: this.sketch.windowHeight,

            };
        },
        draw() {
            let x = this.sketch.frameCount % (40 / this.speed) * 10

            // FPS is 60, but we increase generation only if
            const must_be_generated = this.playing;
            if (must_be_generated) {
                this.generate();
            }

            for (let i = 0; i < this.cols; i++) {
                for (let j = 0; j < this.rows; j++) {
                    if (this.grid[i][j] === 0) {
                        this.sketch.fill(255);
                    } else {
                        this.sketch.fill(0, 255, 255);
                    }
                    this.sketch.square(i * this.size, j * this.size, this.size);
                }
            }
        },
        generate() {
            this.generation_num += 1;
            emitEvent("gol__generation_num", this.generation_num);
        },
        resize() {
            const size = this.get_size()
            this.cols = size.width / this.size;
            this.rows = size.height / this.size;
            this.grid = [];

            // Init array
            for (let i = 0; i < this.cols; i++) {
                this.grid[i] = [];
                for (let j = 0; j < this.rows; j++) {
                    this.grid[i][j] = Math.floor(this.sketch.random(2));
                }
            }
            this.sketch.resizeCanvas(size.width, size.height);
        },
    },
};
