<script lang="ts">
  export default {
    data() {
      return {
        formData: {
          mass: null
        },
        res: '',
        res2: '',
        submitted: false
      };
    },

    methods: {
      submitForm() {
        fetch('http://localhost:443/Calculator', {
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
            let processedData, processedData2;
            if (data.sub60) {
              processedData = `Takeoff Time: ${data.takeoff_time.value} ${data.takeoff_time.unit}`
              processedData2 = `Takeoff Distance: ${data.takeoff_distance.value} ${data.takeoff_distance.unit}`
            } else {
              processedData = `The Payload Is too Heavy!`
              processedData2 = `Excess Payload Mass: ${data.value} ${data.unit}`
            }
            this.res = processedData;
            this.res2 = processedData2;
            console.log('Excess Payload Mass', data);
          })
          .catch(async (error) => {
            console.error('Error:', await error.detail);
          });
        console.log('Form submitted!', this.formData);
        this.submitted = true;
        this.formData.mass = null;
      }
    }
  };
</script>

<template>
  <main class="calc-container">
    <h1>Calculator</h1>
    <br />
    <div class="calc-form">
      <form @submit.prevent="submitForm">
        <div>
          <input type="number" step="any" id="mass" v-model="formData.mass" required placeholder="Payload Mass">
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
    <div class="calc-display" v-if="submitted">
      <p v-text="res"></p>
      <p v-text="res2"></p>
    </div>
  </main>
</template>

<style scoped>
.calc-container {
    position: absolute;
    top: 220px;
    left: 20px;
    height: max-content;
    color: aliceblue;
    border: 2px solid aliceblue;
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(100deg, rgba(55, 55, 55, 0.016), #ac9011);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

  .calc-container h1 {
    color: aliceblue;
  }

  .calc-display {
    height:fit-content;
    color: aliceblue;
    border: 1px solid aliceblue;
    border-radius: 10px;
    background-color: rgb(55, 55, 55);
  }
  .calc-display p {
    padding-left: 2%;
  }

  form input::placeholder {
    color: rgba(255, 255, 255, 0.676);
  }

  form input[type="number"] {
    padding: 10px;
    border: 1px solid aliceblue;
    border-radius: 10px;
    background-color: rgb(55, 55, 55);
    color: aliceblue;
    margin-bottom: 10px;
  }

  form input[type="number"]:focus {
    border-color: white;
  }

  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  form button[type="submit"] {
    background-color: rgb(55, 55, 55);
    color: aliceblue;
    border: 1px solid aliceblue;
    border-radius: 10px;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s, border-color 0.3s, color 0.3s;
  }

  form button[type="submit"]:hover {
    background-color: aliceblue;
    color: rgb(55, 55, 55);
    border-color: transparent;
  }
</style>