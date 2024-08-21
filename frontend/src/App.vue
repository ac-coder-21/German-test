<template>
  <div id="app">
    
    <!-- Start Page -->
    <div v-if="!started">
      <button @click="startTest" class="start-button">
        Start Test
      </button>
      <div class="input-container">
        <label for="jsonFile" class="label">Select JSON File:</label>
        <select
          id="jsonFile"
          v-model="selectedFile"
          class="dropdown-box"
        >
          <option value="" disabled>Select a file</option>
          <option v-for="file in jsonFiles" :key="file" :value="file">
            {{ file }}
          </option>
        </select>
      </div>
    </div>

    <!-- Test Page -->
    <div v-if="started && clickCount < numberOfQuestions && !testCompleted">
      <form @submit.prevent="checkAnswer">
        <div class="input-group">
          <div>
            <label for="english" class="label">English:</label>
            <input type="text" id="english" :value="currentWord.english" readonly class="text-box" />
          </div>

          <div>
            <label for="german" class="label">German:</label>
            <input type="text" id="german" v-model="userInput" class="text-box" />
          </div>
        </div>

        <button type="submit" :disabled="submitDisabled">Submit</button>
      </form>

      <p v-if="resultMessage" :style="{ color: resultColor }">{{ resultMessage }}</p>

      <button v-if="resultMessage && clickCount < numberOfQuestions" @click="nextWord" class="next-word-button">
        Next Word &#8594;
      </button>
    </div>

    <!-- Result Page -->
    <div v-if="testCompleted">
      <p class="completion-message">Test Completed</p>

      <div v-if="wrongAnswers.length > 0">
        <table class="wrong-answers-table">
          <thead>
            <tr>
              <th>Question (English)</th>
              <th class="your-answer">Your Answer</th>
              <th class="correct-answer">Correct Answer (German)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(wrongAnswer, index) in wrongAnswers" :key="index" class="tr-color">
              <td>{{ wrongAnswer.question }}</td>
              <td class="user-wrong-ans">{{ wrongAnswer.yourAnswer }}</td>
              <td class="user-correct-ans">{{ wrongAnswer.correctAnswer }}</td>
            </tr>
          </tbody>
        </table>

        <button @click="takeScreenshot" class="screenshot-button">Take Screenshot</button>
      </div>

      <div v-else>
        <p class="no-wrong-answers-message">No wrong answers, keep it up!!</p>
      </div>

      <button @click="resetTest" class="go-home-button">Go to Home</button>
    </div>
  </div>
</template>

<script>
import html2canvas from 'html2canvas';

export default {
  data() {
    return {
      started: false,
      numberOfQuestions: 5,
      maxQuestions: 0,
      selectedFile: '',
      jsonFiles: ['A1_Nouns', 'A1_Verbs'], // Add your JSON file names here
      currentWord: {
        english: '',
        german: '',
      },
      userInput: '',
      resultMessage: '',
      resultColor: '',
      clickCount: 0,
      wrongAnswers: [],
      fetchedWords: [],
      testCompleted: false,
      submitDisabled: false,
    };
  },
  methods: {
    startTest() {
      if (this.numberOfQuestions < 1) {
        alert('Number of questions must be at least 1.');
        return;
      }
      if (!this.selectedFile) {
        alert('Please select a JSON file.');
        return;
      }
      this.started = true;
      this.clickCount = 0;
      this.wrongAnswers = [];
      this.fetchedWords = [];
      this.testCompleted = false;
      this.submitDisabled = false;
      this.fetchData();
    },
    fetchData() {
      fetch(`http://127.0.0.1:5000/test?file=${this.selectedFile}`)
        .then((response) => response.json())
        .then((data) => {
          this.fetchedWords = data;
          this.maxQuestions = data.length;
          this.numberOfQuestions = Math.min(this.numberOfQuestions, this.maxQuestions);
          this.nextWord();
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
    },
    checkAnswer() {
      if (this.userInput.trim() === this.currentWord.german) {
        this.resultMessage = 'Correct!!!';
        this.resultColor = 'green';
      } else {
        this.resultMessage = 'Wrong!!!';
        this.resultColor = 'red';
        this.wrongAnswers.push({
          question: this.currentWord.english,
          yourAnswer: this.userInput,
          correctAnswer: this.currentWord.german,
        });
      }
      this.submitDisabled = true;
      this.clickCount++;

      if (this.clickCount === this.numberOfQuestions || this.fetchedWords.length === 0) {
        this.testCompleted = true;
      }
    },
    nextWord() {
      if (this.fetchedWords.length > 0) {
        this.currentWord = this.fetchedWords.shift(); // Pop the first element from the array
        this.userInput = '';
        this.resultMessage = '';
        this.resultColor = '';
        this.submitDisabled = false;
      } else {
        this.testCompleted = true;
      }
    },
    resetTest() {
      this.started = false;
      this.numberOfQuestions = 5;
      this.selectedFile = '';
      this.currentWord = { english: '', german: '' };
      this.userInput = '';
      this.resultMessage = '';
      this.resultColor = '';
      this.clickCount = 0;
      this.wrongAnswers = [];
      this.fetchedWords = [];
      this.testCompleted = false;
      this.submitDisabled = false;
    },
    takeScreenshot() {
      html2canvas(document.querySelector('#app')).then(canvas => {
        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');

        link.download = `test-results-${Date.now()}.png`;
        link.click();
      });
    },
  },
};
</script>

<style>
.text-box {
  background-color: white;
  border-radius: 8px;
  color: black;
  font-size: 1.25rem;
  padding: 10px;
  width: 200px;
}

.label {
  font-size: 1.5rem;
  color: #A02334;
}

#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

form {
  text-align: center;
}

.input-group {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.input-group div {
  display: flex;
  flex-direction: column;
  align-items: center;
}

button {
  font-size: 1.5rem;
  padding: 10px 20px;
  margin-top: 20px;
}

p {
  font-size: 1.5rem;
  margin-top: 20px;
}

.next-word-button {
  font-size: 1.5rem;
  padding: 10px 20px;
  margin-top: 10px;
  cursor: pointer;
}

.start-button {
  font-size: 2rem;
  padding: 15px 30px;
  cursor: pointer;
  margin-top: 20px;
  border-radius: 50px;
  background-color: #A02334;
  color: white;
  border: none;
}

.completion-message {
  font-size: 2rem;
  color: #A02334;
  margin-top: 20px;
}

.wrong-answers-table {
  margin-top: 20px;
  border-collapse: collapse;
  width: 100%;
}

.wrong-answers-table th, .wrong-answers-table td {
  border: 1px solid black;
  padding: 10px;
  text-align: left;
}

.wrong-answers-table th {
  background-color: grey;
}

.your-answer {
  color: #eb9594;
}

.correct-answer {
  color: lime;
}

.tr-color {
  color: black;
}

.user-wrong-ans {
  background-color: #eb9594;
}

.user-correct-ans {
  background-color: rgb(128, 247, 128);
}

.input-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-container .label {
  margin-bottom: 10px;
}

.input-container .text-box {
  margin-top: 5px;
}

.no-wrong-answers-message {
  font-size: 1.5rem;
  color: green;
  margin-top: 20px;
}

.go-home-button {
  font-size: 1.5rem;
  padding: 10px 20px;
  margin-top: 20px;
  cursor: pointer;
  background-color: #A02334;
  color: white;
  border: none;
  border-radius: 8px;
}

button:disabled {
  background-color: grey;
  cursor: not-allowed;
}

.screenshot-button {
  font-size: 1.5rem;
  padding: 10px 20px;
  margin-top: 20px;
  cursor: pointer;
  background-color: #A02334;
  color: white;
  border: none;
  border-radius: 8px;
}

.dropdown-box {
  background-color: white;
  border-radius: 8px;
  color: black;
  font-size: 1.25rem;
  padding: 10px;
  width: 200px;
}
</style>
