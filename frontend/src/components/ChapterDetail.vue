
<template>
  <el-container style="height: 700px; border: 1px solid #eee">
    <el-header>
      <el-page-header @back="goBack()" content="详情页面"></el-page-header>
    </el-header>

    <el-main>
      <center>
        <div
          style="white-space: pre-line; line-height:40px; width:1000px; margin：0px auto;"
        >{{content}}</div>
      </center>
    </el-main>
  </el-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Ping",
  data() {
    return {
      content: "",
      msg: ""
    };
  },
  methods: {
    getContent(chapter_id) {
      const path = `http://localhost:5000/cpNlp/api/v1.0/chaptercontent/${chapter_id}`;
      console.log(path);
      axios
        .get(path)
        .then(res => {
          this.content = res.data.content;
          console.log(res);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getContentSeg(chapter_id) {
      const path = `http://localhost:5000/cpNlp/api/v1.0/process/segcontent/${chapter_id}`;
      console.log(path);
      axios
        .get(path)
        .then(res => {
          this.content = res.data.content;
          console.log(res);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getContent(this.$route.query.chapter_id);
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