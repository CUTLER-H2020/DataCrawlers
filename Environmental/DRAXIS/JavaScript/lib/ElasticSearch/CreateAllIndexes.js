const { indexes } = require('./Indexes');
const { Client } = require('@elastic/elasticsearch');
elasticSearchclient = new Client({
  node: 'https://172.16.32.40:9200',
  auth: {
    username: 'wp4',
    password: 'wp4-crawler'
  }
});

const checkIfIndexExist = async index => {
  return new Promise(async resolve => {
    console.log(`Indexing ${index.index}`);
    // if (!res.body) {
    elasticSearchclient.indices
      .create({
        index: index.index,
        body: {
          mappings: {
            _doc: {
              properties: index.mapping
            }
          }
        }
      })
      .then(res => {
        console.log(`Succesfully Created: ${index.index}`);
      })
      .catch(err => {
        console.log(err.body.error);
      });
    // }
  });
};

const initIndexes = (async () => {
  await Promise.all(
    indexes.map(async index => {
      return await checkIfIndexExist(index);
    })
  );
})();
