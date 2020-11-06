<template>
  <div id="wrapper">
    <h1>基于DeepFake First Order Motion的图片转动画项目</h1>
    <hr />
    <img id="logo" src="~@/assets/logo.png" alt="electron-vue" />
    <main>
      <div class="left-side">
        <span class="title">
          选择用于生成动画的图片
          <h6>五官清晰的正脸图片生成效果最佳</h6>
        </span>
        
        <div class="img-upload">
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
          <el-table  :border=true :show-header=false  :data="tableData">
            <el-table-column align="center" width="130">
              <template slot-scope="scope">
                  <div slot="reference" class="name-wrapper">
                    <i class="el-icon-video-play"></i>
                    <span size="medium">{{ scope.row.name }}</span>
                  </div>
              </template>
            </el-table-column>
            <el-table-column align="center" width="150">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="primary"
                  @click="handleEdit(scope.$index, scope.row)">选择</el-button>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)">X</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
      <div class="right-side">
        <div class="general">
          <div class="title">立即开始</div>
          <p>
            阿巴巴巴叭叭叭阿巴巴巴叭叭叭阿巴巴巴叭叭叭阿巴巴巴叭叭叭阿巴巴巴叭叭叭阿巴巴巴叭叭叭阿巴巴巴叭叭叭
          </p>
          <button
            @click="
              general
            "
          >
            开始生成</button
          ><br /><br />
        </div>
        <h5>{{'output:'+command.output}}</h5>
        <h5>{{'err:'+command.err}}</h5>
        <h5>{{'closecode:'+command.closecode}}</h5>
        <h5>{{'exitcode:'+command.exitcode}}</h5>
      </div>
    </main>
  </div>
</template>

<script>
import SystemInformation from './LandingPage/SystemInformation'

export default {
  name: 'landing-page',
  components: { SystemInformation },
  data () {
    return {
      imgpath: 'null',
      command: {
        output: '',
        err: '',
        closecode: 0,
        exitcode: 0
      },
      tableData: [{
        id: 1,
        name: 'Unravel',
        path: '  '
      }, {
        id: 2,
        name: 'Love',
        path: 'null'
      }]
    }
  },
  methods: {
    open (link) {
      this.$electron.shell.openExternal(link)
    },
    handleEdit (index, row) {
      console.log(index, row)
    },
    handleDelete (index, row) {
      console.log(index, row)
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
      let target = path.join(__dirname, '../python/image_animation.py')
      let myvidoe = path.join(__dirname, '../python/1.mp4')
      let checkpoints = path.join(__dirname, '../python/checkpoints/vox-cpk.pth.tar')
      console.log(target)
      // 开启子进程
      var childProcess = require('child_process')
      const process = childProcess.exec('cmd', {stdio: 'pipe'})
      // 编写命令
      let command = 'python ' + target + ' -i ' + this.imgpath + ' -c ' + checkpoints + ' -v ' + myvidoe
      process.stdin.write('activate base\n')
      process.stdin.write(command + '\n')
      process.stdin.end()
      console.log(command)
      // 获取控制台输出
      process.stdout.on('data', function (data) {
        console.log('out:' + data)
        this.command.output = data
      })
      process.stderr.on('data', (data) => {
        console.log('err:' + data)
        this.command.err = data
      })
      process.on('close', function (code) {
        console.log('close code : ' + code)
        this.command.closecode = code
      })
      process.on('exit', (code) => {
        console.log('exit code : ' + code)
        this.command.exitcode = code
      })
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

.left-side {
  display: flex;
  flex-direction: column;
  width: 30px;
  padding-right: 5px;
}

.middle-side {
  display: flex;
  flex-direction: column;
  margin-right: 5%;
  
}
.right-side {
  display: flex;
  flex-direction: column;
  margin-right: 5%;
  
}

.music-list{
  margin-top: 20px;
  width: 282px;
}

.welcome {
  color: #555;
  font-size: 23px;
  margin-bottom: 10px;
}

.title {
  color: #2c3e50;
  font-size: 20px;
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
.img-upload button {
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

label img {
  height: auto;
  margin-top: 20px;
  margin-bottom: 20px;
  width: 200px;
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
