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
            sketch.draw = this.draw;
            sketch.mouseDragged = this.update_drawing;
            sketch.mouseClicked = this.update_drawing;
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
            // let x = this.sketch.frameCount % (40 / this.speed) * 10

            // FPS is 60, but we increase generation only if
            const must_generate_next_grid = this.playing
                && this.sketch.frameCount % Math.floor(10 / this.speed) === 0;
            if (must_generate_next_grid) {
                this.generate_next_grid();
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
        update_drawing() {
            const col = Math.floor(this.sketch.mouseX / this.size);
            const row = Math.floor(this.sketch.mouseY / this.size);

            // Check value exists then update
            if ((this.grid[col] || [])[row] !== undefined) {
                this.grid[col][row] = (this.drawing === "pencil") ? 1 : 0;
            }
        },
        count_neighbors(x, y) {
            let sum = 0;
            for (let i = -1; i < 2; i++) {
                for (let j = -1; j < 2; j++) {
                    let nx = (x + i + this.cols) % this.cols;
                    let ny = (y + j + this.rows) % this.rows;
                    sum += this.grid[nx][ny];
                }
            }
            sum -= this.grid[x][y];
            return sum;
        },
        generate_next_grid() {
            let next_grid = [];
            for (let i = 0; i < this.cols; i++) {
                next_grid[i] = [];
                for (let j = 0; j < this.rows; j++) {
                    let neighbors = this.count_neighbors(i, j);
                    if (this.grid[i][j] === 1 && neighbors < 2) {
                        next_grid[i][j] = 0;
                    } else if (this.grid[i][j] === 1 && (neighbors === 2 || neighbors === 3)) {
                        next_grid[i][j] = 1;
                    } else if (this.grid[i][j] === 1 && neighbors > 3) {
                        next_grid[i][j] = 0;
                    } else if (this.grid[i][j] === 0 && neighbors === 3) {
                        next_grid[i][j] = 1;
                    } else {
                        next_grid[i][j] = this.grid[i][j];
                    }
                }
            }
            this.grid = next_grid;
            this.generation_num += 1;
            emitEvent("gol__generation_num", this.generation_num);
        },
        reset(random = false, width = null, height = null) {
            this.cols = Math.floor((width | this.sketch.width) / this.size);
            this.rows = Math.floor((height | this.sketch.height) / this.size);
            this.grid = [];

            // Init array
            for (let i = 0; i < this.cols; i++) {
                this.grid[i] = [];
                for (let j = 0; j < this.rows; j++) {
                    this.grid[i][j] = (random) ? Math.floor(this.sketch.random(2)) : 0;
                }
            }
        },
        resize() {
            const size = this.get_size()
            this.sketch.resizeCanvas(size.width, size.height);
            this.reset(true, size.width, size.height);
        },
    },
};
