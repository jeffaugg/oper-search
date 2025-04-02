<template>
    <div class="search-container">
      <form @submit.prevent="fetchOperadoras">
        <div class="form-group">
          <label for="uf">UF:</label>
          <input type="text" id="uf" v-model="filters.uf" maxlength="2" placeholder="Ex.: SP" />
        </div>
        <div class="form-group">
          <label for="cidade">Cidade:</label>
          <input type="text" id="cidade" v-model="filters.cidade" placeholder="Ex.: São Paulo" />
        </div>
        <div class="form-group">
          <label for="modalidade">Modalidade:</label>
          <input type="text" id="modalidade" v-model="filters.modalidade" placeholder="Ex.: Administradora de Benefícios" />
        </div>
        <div class="form-group">
          <label for="cnpj">CNPJ:</label>
          <input type="text" id="cnpj" v-model="filters.cnpj" maxlength="14" placeholder="Somente números" />
        </div>
        <div class="form-group">
          <label for="razao_social">Razão Social:</label>
          <input type="text" id="razao_social" v-model="filters.razao_social" placeholder="Ex.: 18 DE JULHO..." />
        </div>
        <button type="submit">Buscar</button>
      </form>
  
      <div class="results">
        <h2>Resultados</h2>
        <ul v-if="operadoras.length">
          <li v-for="operadora in operadoras" :key="operadora.id" class="result-item">
            <p><strong>Razão Social:</strong> {{ operadora.Razao_Social }}</p>
            <p><strong>Registro ANS:</strong> {{ operadora.Registro_ANS }}</p>
            <p><strong>Cidade:</strong> {{ operadora.Cidade }}</p>
            <p><strong>UF:</strong> {{ operadora.UF }}</p>
          </li>
        </ul>
        <p v-else>Nenhum resultado encontrado.</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SearchComponent',
    data() {
      return {
        filters: {
          uf: '',
          cidade: '',
          modalidade: '',
          cnpj: '',
          razao_social: ''
        },
        operadoras: []
      }
    },
    methods: {
      async fetchOperadoras() {
        // Monta a URL com os parâmetros de consulta
        const params = new URLSearchParams()
  
        // Adiciona somente os filtros preenchidos
        Object.keys(this.filters).forEach(key => {
          if (this.filters[key]) {
            params.append(key, this.filters[key])
          }
        })
  
        try {
        const response = await fetch(`/api/v1/operadoras?${params.toString()}`)
          if (!response.ok) {
            throw new Error('Erro ao buscar operadoras')
          }
          this.operadoras = await response.json()
        } catch (error) {
          console.error(error)
          this.operadoras = []
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .search-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 10px;
  }
  form {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    background: #f5f5f5;
    padding: 15px;
    border-radius: 5px;
  }
  .form-group {
    display: flex;
    flex-direction: column;
    flex: 1 1 200px;
  }
  label {
    margin-bottom: 5px;
    font-weight: bold;
  }
  input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  button {
    padding: 10px 20px;
    border: none;
    background: #007bff;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    align-self: flex-end;
  }
  button:hover {
    background: #0056b3;
  }
  .results {
    margin-top: 20px;
  }
  .result-item {
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 10px;
  }
  </style>