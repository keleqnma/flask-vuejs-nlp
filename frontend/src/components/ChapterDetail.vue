
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
              <el-button-group>
                <el-button type="info" icon="el-icon-back" circle @click="jump(-1)"></el-button>
                <el-button type="info" icon="el-icon-right" circle @click="jump(1)"></el-button>
              </el-button-group>

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
                <el-image :src="img" fit="fill">
                  <div slot="placeholder" class="image-slot">
                    加载中
                    <span class="dot">...</span>
                  </div>
                </el-image>
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
      img: "",
      show: Choose.ORIGIN,
      book_id: "",
      chapter_id: "",
      content: "",
      segcontent: [],
      post_segcontent: [],
      ner_content: [],
      senti_content: [],
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
      this.chapter_id = this.img = this.content = "";
      this.segcontent = this.post_segcontent = this.ner_content = this.senti_content = [];
    },
    jump(val) {
      console.log(val);

      this.$router.push({
        path: "/chapters",
        query: {
          chapter_id: Number(this.chapter_id) + Number(val),
          book_id: this.book_id
        }
      });
      this.clear();
      this.routerRefresh();
      this.refresh();
    },
    refresh() {
      this.chapter_id = this.$route.query.chapter_id;
      this.book_id = this.$route.query.book_id;
      console.log("hi" + this.chapter_id);
      this.handleSelect(this.key);
    },
    getner(chapter_id) {
      if (this.ner_content == "") {
        this.getContentSeg(chapter_id);

        const path = `http://localhost:5000/cpNlp/api/v1.0/process/nercontent/${chapter_id}`;
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
    getContent(chapter_id) {
      if (this.content == "") {
        const path = `http://localhost:5000/cpNlp/api/v1.0/chaptercontent/${chapter_id}`;

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
    getContentSeg(chapter_id) {
      if (this.segcontent == "") {
        const path = `http://localhost:5000/cpNlp/api/v1.0/process/segcontent/${chapter_id}`;

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
    getContentSenti(chapter_id) {
      if (this.senti_content == "") {
        const path = `http://localhost:5000/cpNlp/api/v1.0/process/senticontent/${chapter_id}`;

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
    getPostContentSeg(chapter_id) {
      if (this.post_segcontent == "") {
        this.getContentSeg(chapter_id);

        const path = `http://localhost:5000/cpNlp/api/v1.0/process/postagcontentseg/${chapter_id}`;
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
    getWordCloud(chapter_id) {
      if (this.img == "") {
        const path = `http://localhost:5000/cpNlp/api/v1.0/process/wordcloud/${chapter_id}`;
        console.log(path);
        axios
          .get(path)
          .then(res => {
            this.img = "data:image/jpeg;base64," + res.data;
            this.loading = false;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      } else this.loading = false;
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
          this.getWordCloud(this.chapter_id);
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