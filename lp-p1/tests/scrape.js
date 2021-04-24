const fs = require('fs').promises;

fs.readdir('/home/dtc/Downloads/Pacote_Projecto/Testes_publicos').then((folders) => {
  console.log(
    folders
      .map(
        (v, i) => `{
    profile: 'prolog',
    tags: ['public test'],
    description: "Corresponds to test ${v.substring(4)} given by the teacher",
    ...getTest('${i + 1 < 10 ? `0${i + 1}` : `${i + 1}`}'),
  }`
      )
      .join(',')
  );
});
