const fs = require('fs');
const path = require('path');
const os = require('os');
const mooshakDaFeira = require('mooshak-da-feira');

const getTest = (id) => ({
  input: fs.readFileSync(path.resolve(__dirname, 'tests', `test${id}.in`), 'utf-8'),
  output: fs.readFileSync(path.resolve(__dirname, 'tests', `test${id}.out`), 'utf-8'),
});

const commonCode = path.resolve(__dirname, 'codigo_comum.pl');
const publicPuzzles = path.resolve(__dirname, 'puzzles_publicos.pl');

const genProfile = (timeout) => ({
  file: 'program.pl', // file name
  preRunCommands: [`cp ${commonCode} codigo_comum.pl`, `cp ${publicPuzzles} puzzles_publicos.pl`],
  command: `swipl -q -t halt -s program.pl input.pl`, // the command which will be given stdin
  timeout: timeout,
  ignoreNewlinesOnCompare: false,
  preRunHook: ({ test, workingDirectory }) => {
    const input = test.input?.startsWith(':-') ? test.input : `:- ${test.input}`;
    return fs.promises.writeFile(path.resolve(workingDirectory, 'input.pl'), input || '', 'utf-8');
  },
});

mooshakDaFeira({
  workingDirectory: os.tmpdir(),
  profiles: {
    prolog: genProfile(1000),
    prologLong: genProfile(10000),
    prologHyperLong: genProfile(20000),
  },
  tests: [
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 01 given by the teacher',
      ...getTest('01'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 03 given by the teacher',
      ...getTest('02'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 05 given by the teacher',
      ...getTest('03'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 07 given by the teacher',
      ...getTest('04'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 09 given by the teacher',
      ...getTest('05'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 11 given by the teacher',
      ...getTest('06'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 13 given by the teacher',
      ...getTest('07'),
    },
    {
      profile: 'prologLong',
      tags: ['public test'],
      description: 'Corresponds to test 15 given by the teacher',
      ...getTest('08'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 17 given by the teacher',
      ...getTest('09'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 19 given by the teacher',
      ...getTest('10'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 21 given by the teacher',
      ...getTest('11'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 23 given by the teacher',
      ...getTest('12'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 25 given by the teacher',
      ...getTest('13'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 27 given by the teacher',
      ...getTest('14'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 29 given by the teacher',
      ...getTest('15'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 31 given by the teacher',
      ...getTest('16'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 33 given by the teacher',
      ...getTest('17'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 35 given by the teacher',
      ...getTest('18'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 37 given by the teacher',
      ...getTest('19'),
    },
    {
      profile: 'prologLong',
      tags: ['public test'],
      description: 'Corresponds to test 39 given by the teacher',
      ...getTest('20'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 41 given by the teacher',
      ...getTest('21'),
    },
    {
      profile: 'prolog',
      tags: ['public test'],
      description: 'Corresponds to test 43 given by the teacher',
      ...getTest('22'),
    },
    {
      profile: 'prologHyperLong',
      tags: ['public test'],
      description: 'Corresponds to test 45 given by the teacher',
      ...getTest('23'),
    },
  ],
  port: process.env.PORT || 5000,
});
