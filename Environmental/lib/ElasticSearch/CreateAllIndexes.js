const { indexes } = require('./Indexes');
const { Client } = require('@elastic/elasticsearch');
elasticSearchclient = new Client({
  node: 'http://10.10.2.56:9200'
});

const checkIfIndexExist = async index => {
  return new Promise(async resolve => {
    console.log(`Indexing ${index.index}`);
    let res = await elasticSearchclient.indices.exists({
      index: 'cutler_thess_envparameters'
    });
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
        console.log(err.body);
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
