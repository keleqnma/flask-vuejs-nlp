<template>
  <div class="container">
    <h1>小说Nlp</h1>
    <hr />
    <br />
    <div class="search">
      <em>
        <input type="text" placeholder="小说关键字" v-model="keyword" />
        <button type="button" class="btn btn-primary" @click="getKeywordBooks(keyword)">搜索</button>
      </em>
    </div>
    <br />
    <button type="button" class="btn btn-primary" @click="getRandomBook()">换一本书</button>
    <table class="table table-hover">
      <thead>
        <tr>
          <th scope="col">封面</th>
          <th scope="col">书名</th>
          <th scope="col">作者</th>
          <th scope="col">分类</th>
          <th scope="col">简介</th>
          <th scope="col">最后更新</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(book, index) in books" :key="index">
          <td>
            <img :src="book.book_img" />
          </td>
          <td>{{ book.book_name }}</td>
          <td>{{ book.author }}</td>
          <td>{{ book.type }}</td>
          <td>{{ book.profile }}</td>
          <td>{{ book.last_update }}</td>
          <td>
            <div class="btn-group" role="group">
              <button type="button" class="btn btn-danger btn-sm" @click="onDeleteBook(book)">详情</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Ping",
  data() {
    return {
      books: [],
      keyword: "",
      msg: ""
    };
  },
  methods: {
    getRandomBook() {
      const path = `http://localhost:5000/cpNlp/api/v1.0/books`;
      axios
        .get(path)
        .then(res => {
          this.books = res.data.books;
          console.log(this.books);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getKeywordBooks(keyword) {
      const path = `http://localhost:5000/cpNlp/api/v1.0/books/keyword/${keyword}`;
      axios
        .get(path)
        .then(res => {
          this.books = res.data.books;
          console.log(this.books);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getRandomBook();
  }
};
</script>
