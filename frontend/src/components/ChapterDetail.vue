
<template>
  <div class="container">
    <div
      style="text-align: right; font-size: 15px;  background-color: #b3c0d1;
        color: #333;
        line-height: 60px; font-family: Arial"
    >Coco Literarure</div>
    <el-container
      v-loading.fullscreen.lock="fullscreenLoading"
      style="height: 700px; font-family: 微软雅黑;border: 1px solid #eee"
    >
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
                <i class="el-icon-location"></i>
                <span>分词</span>
              </template>
              <el-menu-item index="3-1">原始分词结果</el-menu-item>
              <el-menu-item index="3-2">词性标注分词</el-menu-item>
            </el-submenu>
            <el-menu-item index="4">
              <i class="el-icon-setting"></i>
              <span slot="title">命名实体识别</span>
            </el-menu-item>
            <el-menu-item index="5">
              <i class="el-icon-setting"></i>
              <span slot="title">词云展示</span>
            </el-menu-item>
          </el-menu>
        </el-row>
      </el-aside>

      <el-container class="wraper">
        <el-main>
          <el-backtop target=".wraper">up</el-backtop>
          <center>
            <div
              v-show="show == 1"
              style="white-space: pre-line; line-height:40px; width:900px; "
            >{{content}}</div>
            <div v-show="show == 2" style="white-space: pre-line; line-height:40px; width:900px; ">
              <span v-for="word in segcontent">
                <span>{{word}}</span>
                <el-divider direction="vertical"></el-divider>
              </span>
            </div>
            <div v-show="show == 3" style="white-space: pre-line; line-height:40px; width:900px; ">
              <span v-for="word_post in post_segcontent">
                <el-tooltip
                  class="item"
                  effect="dark"
                  :content="word_post[1]"
                  placement="top-start"
                >
                  <el-button>{{word_post[0]}}</el-button>
                </el-tooltip>
              </span>
            </div>
            <div v-show="show == 5" style="white-space: pre-line; line-height:40px; width:900px; ">
              <el-image :src="img" :fit="fill">
                <div slot="placeholder" class="image-slot">
                  加载中
                  <span class="dot">...</span>
                </div>
              </el-image>
            </div>
          </center>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
var Choose = {
  ORIGIN: 1,
  SEGMENT: 2,
  POSTAG_SEGMENT: 3,
  ENTITY_REC: 4,
  WORD_CLOUD: 5,
  EMOTION: 6
};
export default {
  name: "Ping",
  data() {
    return {
      img: "",
      show: Choose.ORIGIN,
      book_id: "",
      chapter_id: "",
      content: "",
      segcontent: [],
      post_segcontent: [],
      msg: ""
    };
  },
  methods: {
    getContent(chapter_id) {
      if (this.content == "") {
        const path = `http://localhost:5000/cpNlp/api/v1.0/chaptercontent/${chapter_id}`;

        this.fullscreenLoading = true;
        axios
          .get(path)
          .then(res => {
            this.content = res.data.content;
            this.fullscreenLoading = false;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    getContentSeg(chapter_id) {
      if (this.segcontent == "") {
        const path = `http://localhost:5000/cpNlp/api/v1.0/process/segcontent/${chapter_id}`;

        this.fullscreenLoading = true;
        axios
          .get(path)
          .then(res => {
            this.fullscreenLoading = false;
            this.segcontent = res.data.words;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    getPostContentSeg(chapter_id) {
      if (this.post_segcontent == "") {
        const path = `http://localhost:5000/cpNlp/api/v1.0/process/postagcontentseg/${chapter_id}`;

        this.fullscreenLoading = true;
        axios
          .get(path)
          .then(res => {
            this.fullscreenLoading = false;
            this.post_segcontent = res.data.words;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    getWordCloud(chapter_id) {
      if (this.img == "") {
        const path = `http://localhost:5000/cpNlp/api/v1.0/process/wordcloud/${chapter_id}`;
        console.log(path);
        this.fullscreenLoading = true;
        axios
          .get(path)
          .then(res => {
            this.img = "data:image/jpeg;base64," + res.data;
            this.fullscreenLoading = false;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    handleSelect(key) {
      switch (key) {
        case "1": //返回章节列表
          this.$router.push({
            path: "/book",
            query: { book_id: this.book_id }
          });
          break;
        case "2": //原文
          this.show = Choose.ORIGIN;
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
          this.show = Choose.ENTITY_REC;
          break;
        case "5":
          this.show = Choose.WORD_CLOUD;
          this.getWordCloud(this.chapter_id);
          break;
      }
      console.log(key);
    }
  },
  created() {
    this.chapter_id = this.$route.query.chapter_id;
    this.book_id = this.$route.query.book_id;
    this.getContent(this.chapter_id);
  }
};
</script>
<style>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}
</style>