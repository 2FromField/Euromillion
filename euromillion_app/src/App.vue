<template>
  <div class="tirage-form">
    <h2>Sélectionne tes numéros :</h2>

    <div class="main-numbers">
      <label v-for="(number, index) in selectedNumbers" :key="'main-' + index">
        <select v-model="selectedNumbers[index]">
          <option disabled value="">Choisir</option>
          <option v-for="n in 50" :key="n" :value="n">{{ n }}</option>
        </select>
      </label>
    </div>

    <h3>Étoiles :</h3>
    <div class="star-numbers">
      <label v-for="(star, index) in selectedStars" :key="'star-' + index">
        <select v-model="selectedStars[index]">
          <option disabled value="">Choisir</option>
          <option v-for="n in 11" :key="'star-' + n" :value="n">{{ n }}</option>
        </select>
      </label>
    </div>

    <pre>
      Numéros choisis : {{ selectedNumbers }}
      Étoiles choisies : {{ selectedStars }}
    </pre>
  </div>

  <div>
    <h3>Probabilités d'apparition</h3>
    <ul>
      <li v-for="n in selectedNumbers" :key="n">
        Numéro {{ n }} : {{ frequencies.numbers[n] || 0 }} fois ({{
          (((frequencies.numbers[n] || 0) / totalDraws) * 100).toFixed(2)
        }}%)
      </li>

      <li v-for="s in selectedStars" :key="'star-' + s">
        Étoile {{ s }} : {{ frequencies.stars[s] || 0 }} fois ({{
          (((frequencies.stars[s] || 0) / (totalDraws * 2)) * 100).toFixed(2)
        }}%)
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Papa from "papaparse";
import tiragesCsv from "/src/data/euromillion.csv?url";

const selectedNumbers = ref(["", "", "", "", ""]);
const selectedStars = ref(["", ""]);

const frequencies = ref({ numbers: {}, stars: {} });
const totalDraws = ref(0);

function processData(results) {
  const numFreq = {};
  const starFreq = {};

  results.data.forEach((row) => {
    const tirage = row.Tirage?.trim();
    if (!tirage) return;

    const nums = tirage.split(" ").map((n) => parseInt(n));
    if (nums.length < 7) return;

    const mainNumbers = nums.slice(0, 5);
    const stars = nums.slice(5, 7);

    mainNumbers.forEach((n) => {
      if (!isNaN(n)) numFreq[n] = (numFreq[n] || 0) + 1;
    });

    stars.forEach((s) => {
      if (!isNaN(s)) starFreq[s] = (starFreq[s] || 0) + 1;
    });
  });

  totalDraws.value = results.data.length;
  frequencies.value = {
    numbers: numFreq,
    stars: starFreq,
  };
}

onMounted(() => {
  Papa.parse(tiragesCsv, {
    delimiter: ";",
    header: true,
    download: true,
    complete: processData,
  });
});
</script>

<style scoped>
.tirage-form {
  max-width: 600px;
  margin: auto;
  text-align: center;
}

select {
  margin: 5px;
  padding: 6px;
  font-size: 1rem;
}
</style>
