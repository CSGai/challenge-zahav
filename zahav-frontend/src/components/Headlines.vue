<template>
    <main>
        <h1>Tomer's Challenge</h1>
        <h3>Golden Calculator</h3>
    </main>
</template>

<style scoped>
    main {
        position: relative;
        top: 2%;
        left: 1%;
        max-width:fit-content;
        color: aliceblue;
        border: 2px solid aliceblue;
        border-radius: 20px;
        padding: 15px;
        background-color: rgb(56, 56, 56);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    main:hover {
        background-color: rgba(255, 255, 255, 0.09);
        border: 3px solid aliceblue;;
        border-color: white;
    }
    main h3 {
        color:gold;
        animation: glint 4s infinite;
    }
    @keyframes glint {
    0% {
      text-shadow: 0 0 5px gold;
    }
    50% {
      text-shadow: 0 0 20px gold;
    }
    100% {
      text-shadow: 0 0 5px gold;
    }
  }
</style>