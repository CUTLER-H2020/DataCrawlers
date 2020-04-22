const { topics } = require('./Kafka/KafkaTopics');
const util = require('util');
const execFile = require('child_process').execSync;

let arrayTopics = [];

for (const key in topics) {
  if (topics[key].file) {
    arrayTopics.push(topics[key]);
  }
  //   if (topics[key].file == 'anta_soc_visitors_monthly.js') {
  //     const child = execFile(
  //       'node',
  //       [`../${topics[key].file}`],
  //       (error, stdout, stderr) => {
  //         if (error) {
  //           throw error;
  //         }
  //         console.log(stdout);
  //       }
  //     );
  //   }
}

arrayTopics.map(async tp => {
  console.log(`Running ${tp.file}`);

  const { stdout, error } = await execFile('node', [`../${tp.file}`]);

  if (error) {
    throw error;
  }
  console.log(stdout);
});
