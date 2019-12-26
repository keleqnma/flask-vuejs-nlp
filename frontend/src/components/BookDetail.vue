
<template>
  <div>
    <el-container style="height: 700px; font-family: 微软雅黑;border: 1px solid #eee">
      <el-main v-loading.fullscreen.lock="fullscreenLoading">
        <el-page-header @back="goBack" content="详情页面"></el-page-header>
        <div style="line-height: 30px;">
          <img :src="book_information.book_img" class="head_pic" height="120" />
        </div>
        <div style="line-height: 50px;">
          <span style="font-family:微软雅黑; font-size:20px">{{book_information.book_name}}</span>
          <br />

          <el-tag type="success">{{book_information.type}}</el-tag>
          <i style="margin-left: 20px" class="el-icon-edit"></i>
          <span style="margin-left: 10px">{{ book_information.author }}</span>
          <i style="margin-left: 20px" class="el-icon-time"></i>
          <span style="margin-left: 10px">{{ book_information.last_update }}</span>
          <el-link
            style="margin-left: 20px"
            :href="book_information.book_url"
            target="_blank"
            type="success"
            :underline="false"
          >原书链接</el-link>
        </div>
        <el-divider>"{{book_information.profile}}"</el-divider>

        <el-button
          icon="el-icon-notebook-2"
          @click="showdetail(chapter)"
          v-bind:key="chapter.id"
          v-for="chapter in chapters"
        >{{chapter.chapter_name}}</el-button>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Ping",
  data() {
    return {
      book_id: "",
      book_information: {},
      chapters: [],
      keyword: "",
      msg: ""
    };
  },
  methods: {
    goBack() {
      this.$router.push({ path: "/" });
    },
    getChapters(book_id) {
      const path = `/api/chapters/${book_id}`;
      axios
        .get(path)
        .then(res => {
          this.chapters = res.data.chapters;
          console.log(this.chapters);
          this.fullscreenLoading = false;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getBookInformantion(book_id) {
      const path = `/api/books/${book_id}`;
      console.log(path);
      axios
        .get(path)
        .then(res => {
          this.book_information = res.data;
          if (this.book_information.profile == "")
            this.book_information.profile = "暂无简介。";
          console.log(this.book_information);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    showdetail(chapter) {
      if (chapter.chapter_name != "章节已锁定") {
        this.$router.push({
          path: "/chapters",
          query: {
            chapter_id: chapter.id,
            book_id: this.book_id
          }
        });
      } else {
        this.$alert("该内容已被锁定或冻结，暂时无法查看哦！", "提示", {
          confirmButtonText: "确定",
          callback: action => {
            this.$message({
              type: "info",
              message: `action: ${action}`
            });
          }
        });
      }
    }
  },
  created() {
    this.fullscreenLoading = true;
    this.book_id = this.$route.query.book_id;
    this.getBookInformantion(this.book_id);
    this.getChapters(this.book_id);
  }
};
</script>
<style>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 80px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 200px;
}
.el-divider__text {
  position: absolute;
  background-color: #e9eef3;
  padding: 20px;
  color: #303133;
  line-height: 20px;
}
</style>