
<template>
  <div class="container">
    <el-container style="height: 700px; font-family: 微软雅黑;border: 1px solid #eee">
      <el-aside width="250px" :default-openeds="['1', '2','3','4','5']">
        <el-row class="tac">
          <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            @select="handleSelect"
            :default-openeds="['1','2','3','4', '5']"
          >
            <el-menu-item index="1">
              <i class="el-icon-document"></i>
              <span slot="title">返回章节列表</span>
            </el-menu-item>

            <el-menu-item index="2">
              <i class="el-icon-menu"></i>
              <span slot="title">章节原文</span>
            </el-menu-item>
            <el-submenu index="3">
              <template slot="title">
                <i class="el-icon-knife-fork"></i>
                <span>分词</span>
              </template>
              <el-menu-item index="3-1">原始分词结果</el-menu-item>
              <el-menu-item index="3-2">词性标注分词</el-menu-item>
            </el-submenu>
            <el-menu-item index="4">
              <i class="el-icon-postcard"></i>
              <span slot="title">命名实体识别</span>
            </el-menu-item>
            <el-menu-item index="5">
              <i class="el-icon-cloudy"></i>
              <span slot="title">词云展示</span>
            </el-menu-item>
            <el-menu-item index="6">
              <i class="el-icon-film"></i>
              <span slot="title">情感分析</span>
            </el-menu-item>
          </el-menu>
        </el-row>
      </el-aside>

      <el-container>
        <el-main v-loading="loading">
          <div class="wraper">
            <center>
              <el-row>
                <el-button-group>
                  <el-button type="info" icon="el-icon-back" circle @click="jump(-1)"></el-button>
                  <el-button type="info" icon="el-icon-right" circle @click="jump(1)"></el-button>
                </el-button-group>
              </el-row>

              <el-backtop target=".wraper"></el-backtop>
              <div
                v-show="show == 1"
                style="white-space: pre-line; line-height:40px; width:900px; "
              >{{content}}</div>

              <div
                v-show="show == 2"
                style="white-space: pre-line; line-height:40px; width:900px; "
              >
                <div v-for="(words,index) in segcontent" :key="index">
                  <span v-for="(word,index) in words" :key="index">
                    <span style="display: inline-block;">{{word}}</span>
                    <el-divider direction="vertical"></el-divider>
                  </span>
                  <el-divider></el-divider>
                </div>
              </div>

              <div
                v-show="show == 3"
                style="white-space: pre-line; line-height:40px; width:900px; "
              >
                <div v-for="(tags,index1) in post_segcontent" :key="index1">
                  <span v-for="(tag,index2) in tags" :key="index2">
                    <span style="display: inline-block;">
                      <el-tooltip class="item" effect="dark" :content="tag" placement="top-start">
                        <el-button :type="getPostType(tag)">{{segcontent[index1][index2]}}</el-button>
                      </el-tooltip>
                    </span>
                  </span>
                  <el-divider></el-divider>
                </div>
              </div>
              <div
                v-show="show == 4"
                style="white-space: pre-line; line-height:40px; width:900px; "
              >
                <div v-for="(ners,index1) in ner_content" :key="index1">
                  <span v-for="(ner,index2) in ners" :key="index2">
                    <span style="display: inline-block;">
                      <el-tooltip class="item" effect="dark" :content="ner" placement="top-start">
                        <el-button :type="getNerType(ner)">{{segcontent[index1][index2]}}</el-button>
                      </el-tooltip>
                    </span>
                  </span>
                  <el-divider></el-divider>
                </div>
              </div>
              <div
                v-show="show == 5"
                style="white-space: pre-line; line-height:40px; width:900px; "
              >
                <el-row>
                  <el-button type="primary" round @click="getWordCloud(color=1)">蓝青配</el-button>
                  <el-button type="danger" round @click="getWordCloud(color=2)">红白配</el-button>
                  <el-button type="success" round @click="getWordCloud(color=3)">绿白配</el-button>
                  <el-button round @click="getWordCloud(color=4)">随机白</el-button>
                  <el-button type="info" round @click="getWordCloud(color=5)">随机黑</el-button>
                </el-row>
                <canvas
                  id="canvas"
                  width="1500px"
                  height="1200px"
                  style="width:900px;height:600px;"
                ></canvas>
              </div>
              <div
                v-show="show == 6"
                style="white-space: pre-line; line-height:40px; width:900px; "
              >
                <span v-for="(content,index) in senti_content" :key="index">
                  <el-row>
                    <el-col :span="16">
                      <el-link type="info">{{content.sentence}}</el-link>
                    </el-col>
                    <el-col :span="3">
                      <el-tag
                        :type="content.sentiment=='negative'?'danger':'success'"
                      >{{content.sentiment}}</el-tag>
                    </el-col>
                    <el-col :span="5">
                      <el-tag type="info">{{content.degree}}</el-tag>
                    </el-col>
                  </el-row>
                  <el-divider></el-divider>
                </span>
              </div>
            </center>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
import WordCloud from "wordcloud";
import $ from "jquery";
var words = new Array();
var Choose = {
  ORIGIN: 1,
  SEGMENT: 2,
  POSTAG_SEGMENT: 3,
  ENTITY_REC: 4,
  WORD_CLOUD: 5,
  SENTIMENT: 6
};
var map_ner = {
  人名: "primary",
  地名: "warning",
  机构名: "danger",
  无: "info"
};
var map_post = {
  普通名: "primary",
  时间名: "primary",
  方位名: "primary",
  处所名: "primary",
  人名: "success",
  姓: "success",
  名: "success",
  地名: "success",
  族名: "success",
  机构名: "success",
  其他专名: "success",
  动词: "warning",
  趋向动词: "warning",
  联系动词: "warning",
  能愿动词: "warning",
  形容词: "info",
  区别词: "info",
  数词: "info",
  量词: "info",
  副词: "danger",
  代词: "success",
  介词: "info",
  连词: "danger",
  助词: "danger",
  叹词: "danger",
  拟声词: "info",
  习用语: "info",
  缩略语: "info",
  前接成分: "info",
  后接成分: "info",
  语素字: "danger",
  非语素字: "info",
  标点符号: "info",
  非汉字字符串: "info",
  其他未知的符号: "info",
  未知: "info"
};
export default {
  name: "Ping",
  inject: ["routerRefresh"],
  data() {
    return {
      key: "2",
      wordFreqs: [],
      show: Choose.ORIGIN,
      book_id: "",
      chapter_id: "",
      content: "",
      segcontent: [],
      post_segcontent: [],
      ner_content: [],
      senti_content: [],
      chapters: [],
      loading: true
    };
  },
  methods: {
    getPostType(type) {
      return map_post[type];
    },
    getNerType(type) {
      return map_ner[type];
    },
    clear() {
      this.chapter_id = this.content = this.wordFreqs = this.segcontent = this.post_segcontent = this.ner_content = this.senti_content =
        "";
    },
    jump(val) {
      console.log(val);
      console.log("next chapter");
      var next_chapter_id = Number(this.chapter_id) + Number(val);
      var next_chapter = this.chapters.filter(function(e) {
        return e.id == next_chapter_id;
      });
      if (next_chapter.length == 0) {
        this.$alert("没了", "提示", {
          confirmButtonText: "确定",
          callback: action => {
            this.$message({
              type: "info",
              message: `action: ${action}`
            });
          }
        });
      } else if (next_chapter[0].chapter_name == "章节已锁定") {
        this.$alert("该内容已被锁定或冻结，暂时无法查看哦！", "提示", {
          confirmButtonText: "确定",
          callback: action => {
            this.$message({
              type: "info",
              message: `action: ${action}`
            });
          }
        });
      } else {
        this.$router.push({
          path: "/chapters",
          query: {
            chapter_id: next_chapter_id,
            book_id: this.book_id
          }
        });
      }
      this.clear();
      this.routerRefresh();
      this.refresh();
    },
    refresh() {
      this.chapter_id = this.$route.query.chapter_id;
      this.book_id = this.$route.query.book_id;
      console.log("hi" + this.chapter_id);
      this.handleSelect(this.key);
      this.getChapters(this.book_id);
    },
    getner(chapter_id = this.chapter_id) {
      if (this.ner_content == "") {
        if (this.segcontent == "") {
          const path = `/api/process/segcontent/${chapter_id}`;

          axios.get(path).then(res => {
            this.segcontent = res.data.words;
          });
        }
        const path = `/api/process/nercontent/${chapter_id}`;
        this.loading = true;
        axios
          .get(path)
          .then(res => {
            this.ner_content = res.data.ners;
            this.loading = false;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      } else this.loading = false;
    },
    getChapters(book_id) {
      const path = `/api/chapters/${book_id}`;
      axios
        .get(path)
        .then(res => {
          this.chapters = res.data.chapters;
          this.fullscreenLoading = false;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getContent(chapter_id = this.chapter_id) {
      if (this.content == "") {
        const path = `/api/chaptercontent/${chapter_id}`;

        axios
          .get(path)
          .then(res => {
            this.content = res.data.content;
            this.loading = false;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      } else this.loading = false;
    },
    getContentSeg(chapter_id = this.chapter_id) {
      if (this.segcontent == "") {
        const path = `/api/process/segcontent/${chapter_id}`;

        axios
          .get(path)
          .then(res => {
            this.segcontent = res.data.words;
            this.loading = false;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      } else this.loading = false;
    },
    getContentSenti(chapter_id = this.chapter_id) {
      if (this.senti_content == "") {
        const path = `/api/process/senticontent/${chapter_id}`;

        axios
          .get(path)
          .then(res => {
            this.senti_content = res.data.sentiments;
            this.loading = false;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      } else this.loading = false;
    },
    getPostContentSeg(chapter_id = this.chapter_id) {
      if (this.post_segcontent == "") {
        if (this.segcontent == "") {
          const path = `/api/process/segcontent/${chapter_id}`;

          axios.get(path).then(res => {
            this.segcontent = res.data.words;
          });
        }

        const path = `/api/process/postagcontentseg/${chapter_id}`;
        this.loading = true;
        axios
          .get(path)
          .then(res => {
            this.post_segcontent = res.data.tags;
            this.loading = false;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      } else this.loading = false;
    },
    getImages(color) {
      var wordFreqs = this.wordFreqs;
      var background_color = "";
      var plain_color = "";
      var important_color = "";
      var color_var = "";
      switch (color) {
        case 1:
          background_color = "#e9eef3";
          plain_color = "#b3c0d1";
          important_color = "#116de6";
          break;
        case 2:
          background_color = "#ffe0e0";
          plain_color = "#c09292";
          important_color = "#f02222";
          break;
        case 3:
          background_color = "#E2FAE7";
          plain_color = "#82A088";
          important_color = "#63D0A4";
          break;
        case 4:
          background_color = "#e9eef3";
          color_var = "random-dark";
          break;
        case 5:
          background_color = "#2D365B";
          color_var = "random-light";
          break;
      }
      var max_3_freq = wordFreqs[2].count;
      var canvas = document.getElementById("canvas");
      var color_func = function(word, weight) {
        return weight >= max_3_freq ? important_color : plain_color;
      };

      var options = eval({
        list: words,
        gridSize: Math.round((16 * $("#canvas").width()) / 1024), // 密集程度 数字越小越密集
        weightFactor: function(size) {
          return (Math.pow(size, 0.7) * $("#canvas").width()) / 32;
        }, // 字体大小=原始大小*weightFactor
        maxFontSize: 100, //最大字号
        minFontSize: 30, //最小字号
        rotationSteps: 2,
        fontWeight: "normal", //字体粗细
        fontFamily: "Times, serif", // 字体
        color: color >= 4 ? color_var : color_func, // 字体颜色 'random-dark' 或者 'random-light'
        backgroundColor: background_color, // 背景颜色
        rotateRatio: 0.5 // 字体倾斜(旋转)概率，1代表总是倾斜(旋转)
      });
      //生成
      WordCloud(canvas, options);
      this.loading = false;
    },
    getWordCloud(color, chapter_id = this.chapter_id) {
      console.log("color" + color);
      if (this.wordFreqs == "") {
        const path = `/api/process/wordcloud/${chapter_id}`;
        console.log(path);
        axios
          .get(path)
          .then(res => {
            this.wordFreqs = res.data;
            var wordFreqs = this.wordFreqs;
            for (var i = 0; i < wordFreqs.length; i++) {
              var option = [wordFreqs[i].word, wordFreqs[i].count];
              words.push(option);
            }
            this.getImages(color);
          })
          .catch(error => {
            console.error(error);
          });
      } else this.getImages(color);
    },
    handleSelect(key) {
      this.loading = true;
      this.key = key;

      switch (key) {
        case "1": //返回章节列表
          this.$router.push({
            path: "/book",
            query: { book_id: this.book_id }
          });
          break;
        case "2": //原文
          this.show = Choose.ORIGIN;
          this.getContent(this.chapter_id);
          break;
        case "3-1": //分词
          this.getContentSeg(this.chapter_id);
          this.show = Choose.SEGMENT;
          break;
        case "3-2":
          this.getPostContentSeg(this.chapter_id);
          this.show = Choose.POSTAG_SEGMENT;
          break;
        case "4":
          this.getner(this.chapter_id);
          this.show = Choose.ENTITY_REC;
          break;
        case "5":
          this.show = Choose.WORD_CLOUD;
          this.getWordCloud(1);
          break;
        case "6":
          this.show = Choose.SENTIMENT;
          this.getContentSenti(this.chapter_id);
          break;
      }
      console.log(key);
    }
  },
  created() {
    this.refresh();
  }
};
</script>
<style>
.el-aside {
  color: #333;
}

.wraper {
  height: 100vh;
  height: 660px;
  overflow: hidden;
  overflow-x: hidden;
  overflow-y: scroll;
}
</style>