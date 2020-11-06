<template>
  <div id="wrapper">
    <h1>基于DeepFake First Order Motion的图片转动画项目</h1>
    <hr />
    <img id="logo" src="~@/assets/logo.png" alt="electron-vue" />
    <main>
      <div class="left-side">
        <div class="general">
          <div class="title">选择用于生成动画的图片</div>
           <p>五官清晰的正脸图片生成效果最佳</p>
        </div>
        <div class="img-upload zoom-out">
          <input
            type="file"
            id="myimg"
            @change="chooseFile($event)"
            accept="image/*"
            style="display: none"
          />
          <label for="myimg">
            <img src="~@/assets/face.png" alt="img" />
          </label>
          <h4>{{'图片地址 : '+imgpath}}</h4>
        </div>
        <system-information></system-information>
      </div>
      <div class="middle-side">
        <span class="title">
          选择用于生成动画的音乐模板
        </span>
        <div class="music-list">
          <el-table  :border=true :show-header=false  :data="videoData" :fit=true>
            <el-table-column align="center" >
              <template slot-scope="scope">
                  <div slot="reference" class="name-wrapper">
                    <i class="el-icon-video-play"></i>
                    <span size="medium">{{ scope.row.name }}</span>
                  </div>
              </template>
            </el-table-column>
            <el-table-column align="center" >
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  :type="currVideoId==scope.row.id?'success':'nomal'"
                  @click="selectVideo(scope.$index, scope.row)">{{currVideoId==scope.row.id?'已选':'选择'}}</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <br /><br />
        <h4>{{'模板地址 : '+videopath}}</h4>
      </div>
      <div class="right-side">
        <div class="general">
          <div class="title">立即开始</div>
          <p>
            视频生成速度由GPU性能决定，若环境中没有配置好CUDA则无法加速渲染，由GPU处理所需时长3-5分钟不等，若用CPU处理则需几小时。
          </p>
          <br />
          <button
            @click="
              general
            "
          >
            开始生成</button
          ><br /><br />

        </div>
        <video :src="videopath" width="200" height="auto" controls>您的电脑不支持video标签
        </video>
        <h5>{{'output:'+commandMsg.output}}</h5>
        <h5>{{'err:'+commandMsg.err}}</h5>
        <h5>{{'closecode:'+commandMsg.closecode}}</h5>
        <h5>{{'exitcode:'+commandMsg.exitcode}}</h5>
      </div>
    </main>
  </div>
</template>
<script src="./video_tool.js"></script>
<script>
import SystemInformation from './LandingPage/SystemInformation'

export default {
  name: 'landing-page',
  components: { SystemInformation },
  data () {
    return {
      currVideoId: 0,
      imgpath: 'null',
      videopath: 'D:' + '\\360MoveData\\Users\\chen6\\Desktop\\vue-electron\\pic2animation\\src\\renderer\\python\\Inputs\\1.mp4',
      commandMsg: {
        output: '',
        err: '',
        closecode: 6,
        exitcode: 6
      },
      videoData: [{
        id: 1,
        name: 'Unravel-女声'
      }, {
        id: 2,
        name: 'The spectre-女声'
      }, {
        id: 3,
        name: '达拉崩吧'
      }]
    }
  },
  methods: {
    open (link) {
      this.$electron.shell.openExternal(link)
    },
    // 选择视频模板
    selectVideo (index, row) {
      this.currVideoId = index + 1
      console.log(index, row)
      this.videopath = '../python/Inputs/' + this.videoData[index].id + '.mp4'
      console.log(this.videopath)
    },
    // 图片选择组件
    chooseFile (e) {
      var currentImg = e.target.nextElementSibling.childNodes[0]
      currentImg.setAttribute(
        'src', window.URL.createObjectURL(e.target.files[0])
      )
      // 获取图片路径
      const files = e.target.files
      const file = files[0]
      const path = file.path
      console.log(path)
      this.imgpath = path
      currentImg.onload = function () {
        window.URL.revokeObjectURL(this.src)
      }
    },
    // 控制台调用Python
    general () {
      const path = require('path')
      // Python脚本和资源模型的路径
      let targetVideoPath = path.join(__dirname, this.videopath)
      let target = path.join(__dirname, '../python/image_animation.py')
      let testTarget = path.join(__dirname, '../python/test.py')
      let checkpoints = path.join(__dirname, '../python/checkpoints/vox-cpk.pth.tar')
      console.log(target)
      // 开启子进程
      var childProcess = require('child_process')
      const process = childProcess.exec('cmd', {stdio: 'pipe'})
      // 编写命令
      let command = 'python ' + target + ' -i ' + this.imgpath + ' -c ' + checkpoints + ' -v ' + targetVideoPath
      let testCmd = 'python ' + testTarget
      process.stdin.write('activate base\n')
      process.stdin.write(testCmd + '\n')
      process.stdin.write(command + '\n')
      process.stdin.end()
      console.log(command)
      // 获取控制台输出
      process.stdout.on('data', (out) => {
        console.log('out:' + out)
        this.commandMsg.output = out
        let msg = out.split(':')
        if (msg[0] === 'python') {
          if (msg[1] === 'finish') {
            // 视频生成完成
          }
        }
        // 获取到生成的视频的路径
        if (msg[0] === 'finalvideo') {
          this.videopath = msg[1] + ':' + msg[2]
        }
      })
      process.stderr.on('data', (err) => {
        console.log('err:' + err)
        this.commandMsg.err = err
      })
      process.on('close', (closecode) => {
        console.log('close code : ' + closecode)
        this.commandMsg.closecode = closecode
      })
      process.on('exit', (code) => {
        console.log('exit code : ' + code)
        this.commandMsg.exitcode = code
      })
    },
    playVideo () {
      var vdo = document.getElementById('videoPlay')
      vdo.play()
    }

  }
}
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300&display=swap");
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body {
  font-family: 'Noto Sans SC', sans-serif;
}
#wrapper {
  background: radial-gradient(
    ellipse at top left,
    rgba(255, 255, 255, 1) 40%,
    rgba(229, 229, 229, 0.9) 100%
  );
  height: 100vh;
  padding: 60px 80px;
  width: 100vw;
}

#logo {
  height: auto;
  margin-top: 20px;
  margin-bottom: 20px;
  width: 200px;
}

main {
  display: flex;
  justify-content: space-around;
}

main > div {
  flex-basis: 50%;
}
.zoom-out img:hover{
  cursor: pointer;  
  transition: all 0.3s;
	transform: scale(1.1);
}
.left-side {
  display: flex;
  flex-direction: column;
  max-width: 400px;
  padding-right: 5px;
}

.middle-side {
  display: flex;
  flex-direction: column;
  margin-right: 5%;
  max-width: 400px;
}
.el-button:focus, .el-button:hover {
    color: #4fc08d;
    border-color: #6dc4a0;
    background-color: #ecfff7;
}
.el-button--success {
    color: #FFF;
    background-color: #4fc08d;
    border-color: #4fc08d;
}
.el-button--success:focus, .el-button--success:hover {
    background: #5fc798;
    border-color:#5fc798;
    color: #FFF;
}
.right-side {
  display: flex;
  flex-direction: column;
  margin-right: 5%;
  
}

.music-list{
  margin-top: 20px;
}

.welcome {
  color: #555;
  font-size: 23px;
  margin-bottom: 10px;
}

.title {
  color: #2c3e50;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 6px;
}

.title.alt {
  font-size: 18px;
  margin-bottom: 10px;
}

.general p {
  color: black;
  margin-bottom: 10px;
}

.general button {
  font-size: 1.2em;
  font-family: 'Noto Sans SC', sans-serif;
  cursor: pointer;
  outline: none;
  padding: 0.75em 2em;
  border-radius: 2em;
  display: inline-block;
  color: #fff;
  background-color: #4fc08d;
  transition: all 0.15s ease;
  box-sizing: border-box;
  border: 1px solid #4fc08d;
}
.img-upload button {
  font-size: 0.8em;
  font-family: 'Noto Sans SC', sans-serif;
  cursor: pointer;
  outline: none;
  padding: 0.75em 2em;
  border-radius: 2em;
  display: inline-block;
  color: #fff;
  background-color: #4fc08d;
  transition: all 0.15s ease;
  box-sizing: border-box;
  border: 1px solid #4fc08d;
}

label img {
  height: auto;
  margin-top: 20px;
  margin-bottom: 20px;
  width: 200px;
  border-radius: 20px;
}

input button {
  font-size: 0.8em;
  cursor: pointer;
  outline: none;
  padding: 0.75em 2em;
  border-radius: 2em;
  display: inline-block;
  color: #fff;
  background-color: #4fc08d;
  transition: all 0.15s ease;
  box-sizing: border-box;
  border: 1px solid #4fc08d;
}

.general button.alt {
  color: #42b983;
  background-color: transparent;
}
</style>
