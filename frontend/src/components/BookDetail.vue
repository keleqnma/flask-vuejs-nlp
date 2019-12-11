
<template>
  <el-container style="height: 700px; border: 1px solid #eee">
    <el-page-header @back="goBack" content="详情页面"></el-page-header>
    <el-header>
      <p style="font-family:Helvetica Neue">Coco literature</p>
    </el-header>

    <el-main>
      <el-button
        icon="el-icon-notebook-2"
        @click="showdetail(chapter)"
        v-bind:key="chapter.id"
        v-for="chapter in chapters"
      >{{chapter.chapter_name}}</el-button>
    </el-main>
  </el-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Ping",
  data() {
    return {
      chapters: [],
      keyword: "",
      msg: ""
    };
  },
  methods: {
    getChapters(book_id) {
      const path = `http://localhost:5000/cpNlp/api/v1.0/chapters/${book_id}`;
      axios
        .get(path)
        .then(res => {
          this.chapters = res.data.chapters;
          console.log(this.chapters);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    showdetail(chapter) {
      this.$router.push({
        path: "/chapters",
        query: {
          chapter_id: chapter.id
        }
      });
    }
  },
  created() {
    this.name = this.$route.query.book_name;
    this.getChapters(this.$route.query.book_id);
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
</style>