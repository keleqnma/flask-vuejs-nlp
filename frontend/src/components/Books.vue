
<template style="margin-top: 0px;">
  <div class="container">
    <el-container
      class="ui-widget-container"
      direction="vertical"
      style="height: 700px; font-family: 微软雅黑;border: 1px solid #eee"
    >
      <el-main>
        <center style="line-height: 70px;">
          <el-row :gutter="5">
            <el-col :span="20">
              <el-input size="big" placeholder="请输入关键字" v-model="keyword" clearable></el-input>
            </el-col>
            <el-col :span="4">
              <el-button
                type="primary"
                icon="el-icon-search"
                @click="getKeywordBooks(keyword)"
                v-loading.fullscreen.lock="fullscreenLoading"
              >搜索</el-button>
            </el-col>
          </el-row>
        </center>
        <div style="margin: 50px 0;">
          <el-divider>
            <el-button
              type="primary"
              icon="el-icon-magic-stick"
              @click="getRandomBook()"
              v-loading.fullscreen.lock="fullscreenLoading"
              circle
            ></el-button>
          </el-divider>
        </div>
        <div>
          <div
            style="line-height: 40px; background-color: #FFF;"
            v-bind:key="book.id"
            v-for="book in books"
          >
            <br />
            <el-row>
              <el-col :span="4">
                <img :src="book.book_img" class="head_pic" height="120" />
              </el-col>
              <el-col :span="4">
                <span
                  style="font-family:微软雅黑; font-size:20px;margin-left: 20px"
                >{{ book.book_name }}</span>
              </el-col>
              <el-col :span="3">
                <i style="margin-left: 20px" class="el-icon-edit"></i>
                <span style="margin-left: 10px">{{ book.author }}</span>
              </el-col>
              <el-col :span="2">
                <el-tag type="success" style="margin-left: 20px">{{book.type}}</el-tag>
              </el-col>

              <el-col :span="4">
                <span style="margin-left: 20px">{{ book.profile }}</span>
              </el-col>
              <el-col :span="4">
                <i style="margin-left: 20px" class="el-icon-time"></i>
                <span style="margin-left: 10px">{{ book.last_update }}</span>
              </el-col>

              <el-col :span="3">
                <el-button icon="el-icon-notebook-2" @click="showdetail(book)"></el-button>
              </el-col>
            </el-row>
            <el-divider></el-divider>
          </div>
        </div>
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
      fullscreenLoading: false,
      books: [],
      keyword: "",
      msg: ""
    };
  },
  methods: {
    getRandomBook() {
      this.fullscreenLoading = true;
      const path = "/api/books";
      console.log(path);
      axios
        .get(path)
        .then(res => {
          this.books = res.data.books;
          this.fullscreenLoading = false;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getKeywordBooks(keyword) {
      this.fullscreenLoading = true;
      const path = `/api/books/keyword/${keyword}`;
      axios
        .get(path)
        .then(res => {
          this.books = res.data.books;
          this.fullscreenLoading = false;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    showdetail(book) {
      this.$router.push({
        path: "/book",
        query: { book_id: book.id }
      });
    }
  },
  created() {
    this.getRandomBook();
  }
};
</script>
