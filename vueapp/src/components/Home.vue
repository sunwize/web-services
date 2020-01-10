<template>
  <div>
    <b-container>
      <b-input-group class="my-3">
        <b-form-input type="text" v-model="search" placeholder="ex: Quafafou"></b-form-input>

        <b-input-group-append>
          <b-button @click="searchByCoAuthors" v-b-popover.hover.top="'Rechercher les co-auteurs'" :variant="button1Variant"><icon icon="user-tie"></icon></b-button>
        </b-input-group-append>

        <b-input-group-append>
          <b-button @click="searchBySources" v-b-popover.hover.top="'Rechercher les sources'" :variant="button2Variant"><icon icon="book"></icon></b-button>
        </b-input-group-append>
      </b-input-group>

      <b-tabs content-class="mt-3" fill>
        <b-tab title="HAL">
          <div v-if="hal.length === 0">
            Pas de résultat
          </div>
          <b-list-group v-else class="text-left">
            <b-list-group-item class="font-weight-bold">
              <div v-if="search_mode === 1" class="d-flex">
                <span style="width: 100%">Sources</span>
              </div>
              <div v-else class="d-flex">
                <span style="width: 20%">Co-autheurs</span>
                <span style="width: 80%">Source</span>
              </div>
            </b-list-group-item>
            <b-list-group-item v-for="(el, index) in hal" :key="index">
              <a v-if="search_mode === 1" class="text-primary" :href="el.url"><icon icon="book"></icon> {{ el.title }}</a>
              <div v-else class="d-flex">
                <span style="width: 20%"><icon icon="user-tie"></icon> {{ el.name }}</span>
                <span style="width: 80%"><icon icon="book"></icon> {{ el.source }}</span>
              </div>
            </b-list-group-item>
          </b-list-group>
        </b-tab>
        <b-tab title="Arxiv">
          <div v-if="arxiv.length === 0">
            Pas de résultat
          </div>
          <b-list-group v-else class="text-left">
            <b-list-group-item class="font-weight-bold">
              <div v-if="search_mode === 1" class="d-flex">
                <span style="width: 100%">Sources</span>
              </div>
              <div v-else class="d-flex">
                <span style="width: 20%">Co-autheurs</span>
                <span style="width: 80%">Source</span>
              </div>
            </b-list-group-item>
            <b-list-group-item v-for="(el, index) in arxiv" :key="index">
              <a v-if="search_mode === 1" class="text-primary" :href="el.url"><icon icon="book"></icon> {{ el.title }}</a>
              <div v-else class="d-flex">
                <span style="width: 20%"><icon icon="user-tie"></icon> {{ el.name }}</span>
                <span style="width: 80%"><icon icon="book"></icon> {{ el.source }}</span>
              </div>
            </b-list-group-item>
          </b-list-group>
        </b-tab>
      </b-tabs>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data: function () {
    return {
      search: '',
      search_mode: -1,
      hal: [],
      arxiv: []
    }
  },
  computed: {
    button1Variant: function () {
      if (this.search_mode === 0) { return 'secondary' } else { return 'outline-secondary' }
    },
    button2Variant: function () {
      if (this.search_mode === 1) { return 'secondary' } else { return 'outline-secondary' }
    }
  },
  methods: {
    searchByCoAuthors: function () {
      this.hal = []
      this.arxiv = []
      this.search_mode = 0
      if (this.search === '') {
        return
      }
      axios.get('https://halarxiv.azurewebsites.net/hal/coauthors/' + this.search).then(resp => {
        this.hal = resp.data
      })
      axios.get('https://halarxiv.azurewebsites.net/arxiv/coauthors/' + this.search).then(resp => {
        this.arxiv = resp.data
      })
    },
    searchBySources: function () {
      this.hal = []
      this.arxiv = []
      this.search_mode = 1
      if (this.search === '') {
        return
      }
      axios.get('https://halarxiv.azurewebsites.net/hal/sources/' + this.search).then(resp => {
        this.hal = resp.data
      })
      axios.get('https://halarxiv.azurewebsites.net/arxiv/sources/' + this.search).then(resp => {
        this.arxiv = resp.data
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
