<template>
    <div id="app">
      <h1>Consulta de Operadoras de Saúde</h1>
      <SearchComponent />
    </div>
  </template>
  
  <script>
  import SearchComponent from './components/SearchComponent.vue'
  
  export default {
    name: 'App',
    components: {
      SearchComponent
    }
  }
  </script>
  
  <style>
  #app {
    font-family: Arial, sans-serif;
    margin: 20px;
  }
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  </style>