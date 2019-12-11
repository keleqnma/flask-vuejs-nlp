
<template>
  <el-container class="ui-widget-container" direction="vertical">
    <el-header>
      <p style="font-family:Helvetica Neue">Coco literature</p>
    </el-header>

    <el-main>
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
    </el-main>

    <el-main>
      <el-table :data="books" style="width: 100%">
        <el-table-column v-bind="item" v-for="(item, index) in columns" :key="index"></el-table-column>
      </el-table>

      <el-table :data="books">
        <el-table-column label="封面" width="150">
          <template slot-scope="scope">
            <img :src="scope.row.book_img" class="head_pic" height="120" />
          </template>
        </el-table-column>
        <el-table-column label="书名">
          <template slot-scope="scope">
            <p style="font-family:微软雅黑; font-size:20px">{{ scope.row.book_name }}</p>
          </template>
        </el-table-column>
        <el-table-column label="作者" width="180">
          <template slot-scope="scope">
            <i class="el-icon-edit"></i>
            <span style="margin-left: 10px">{{ scope.row.author }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="分类" width="80"></el-table-column>
        <el-table-column prop="profile" label="简介"></el-table-column>
        <el-table-column label="最后更新">
          <template slot-scope="scope">
            <i class="el-icon-time"></i>
            <span style="margin-left: 10px">{{ scope.row.last_update }}</span>
          </template>
        </el-table-column>

        <el-table-column align="right" width="80">
          <template slot="header" slot-scope="scope">
            <el-button
              type="primary"
              icon="el-icon-magic-stick"
              @click="getRandomBook()"
              v-loading.fullscreen.lock="fullscreenLoading"
            ></el-button>
          </template>
          <template slot-scope="scope">
            <el-button icon="el-icon-notebook-2" @click="showdetail(scope.row)"></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
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
      const path = `http://localhost:5000/cpNlp/api/v1.0/books`;
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
      const path = `http://localhost:5000/cpNlp/api/v1.0/books/keyword/${keyword}`;
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
<style>
.ui-widget-container {
  .container-header,
  .container-main {
    background-color: #fff;
    border-radius: 3px;
    box-shadow: 0 0 1px 1px rgba(0, 0, 0, 0.03);
  }
  .container-header {
    padding: 15px 10px;
    margin-bottom: 20px;
  }
}
</style>