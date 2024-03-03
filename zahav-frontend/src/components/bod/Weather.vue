<script lang="ts">
  export default {
    data() {
      return {
        formData: {
          date: null
        },
        res: '',
        submitted: false
      };
    },

    methods: {
      postDate() {
        fetch('http://localhost:443/api/weather', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.formData)
          })
          .then(async response => {
            const jres = await response.json()
            if (!response.ok) {
              throw jres;
            }
            return jres;
          })
          .then(data => {
            console.log('You may take off at:', data);
            this.res = 'you may take-off at the following hours:';
            data.forEach((element: string) => {
              this.res += ' ' + element;
            });
          })
          .catch(async (error) => {
            console.error('Error:', await error.detail);
            this.res = error.detail.replace('400:', '');
          });
        console.log('Form submitted!', this.formData);
        this.submitted = true;
      }
    }
  };
</script>

<template>
  <main>
    <h1>Weather</h1>
    <br>
    <input type="date" v-model="formData.date" @change="postDate">
    <div v-if="res" class="weather-display">
      <p v-text="res"></p>
    </div>
  </main>
</template>

<style scoped>
  .weather-display p {
    padding-left: 2%;
  }
  .weather-display {
    margin-top: 22%;
    height: fit-content;
    color: aliceblue;
    border: 1px solid aliceblue;
    border-radius: 10px;
    background-color: rgb(55, 55, 55);
  }
  main {
    color: aliceblue;
    border: 1px solid aliceblue;
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(100deg, #ac9011, rgba(55, 55, 55, 0.016));
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  main input[type="date"] {
    padding: 10px;
    border: 1px solid aliceblue;
    border-radius: 10px;
    background-color: rgb(55, 55, 55);
    color: aliceblue;
    margin-bottom: 10px;
  }

  .response {
    display: inline-block;
    margin-top: 10px;
  }
</style>