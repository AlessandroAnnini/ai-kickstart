import OpenAI from 'openai';
import readline from 'node:readline';

const openai = new OpenAI({ apiKey: process.env['OPENAI_API_KEY'] });

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const getUserMessage = () =>
  new Promise((resolve) => {
    rl.question('> ', (question) => {
      resolve(question);
    });
  });

const context = [];
context.push({ role: 'system', content: 'You are a useful assistant' });

///////////////////////////
// functions
// https://openlibrary.org/swagger/docs
///////////////////////////

/**
 * Fetch books by subject name.
 * making a call to the Open Library Books API.
 * GET https://openlibrary.org/subjects/{subject}.json?details=false
 *
 * @param {string} subject - The subject to search for.
 * @returns {object} - The response object.
 */

async function fetchBooksBySubject({ subject }) {
  const url = `https://openlibrary.org/subjects/${subject}.json?details=false`;
  const response = await fetch(url);
  const data = await response.json();
  return data;
}

const services = {
  fetchBooksBySubject,
};

///////////////////////////
// functions definitions
///////////////////////////

const functions = [
  {
    name: 'fetchBooksBySubject',
    description: 'Fetch books by subject name.',
    parameters: {
      type: 'object',
      properties: {
        subject: {
          type: 'string',
          description: 'The subject to search for.',
        },
      },
      required: ['subject'],
    },
  },
];

///////////////////////////
// chat loop
///////////////////////////

while (true) {
  const question = await getUserMessage();

  if (question === 'bye') {
    process.exit();
  }

  context.push({ role: 'user', content: question });

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    temperature: 0.2,
    messages: context,
    functions,
    function_call: 'auto',
  });

  console.log(JSON.stringify(response, null, 2));

  console.log('\n');

  ///////////////////////////
  // function_call
  ///////////////////////////

  if (response.choices[0].message.function_call) {
    console.log('🤖 Function call:');
    const fc = response.choices[0].message.function_call;
    console.log(`function name: ${fc.name}`);
    console.log(`function args: ${fc.arguments}`);
    console.log('\n');

    // const args = JSON.parse(fc.arguments);
    // const resp = await services[fc.name](args);
    // console.log(resp);

    if (fc.name === 'fetchBooksBySubject') {
      const args = JSON.parse(fc.arguments);
      console.log(`🤖 ${fc.arguments}`);
      const book_list = await fetchBooksBySubject(args);

      for (const book of book_list.works) {
        console.log(`${book.first_publish_year} - ${book.title}`);
      }
    }

    continue;
  }

  ///////////////////////////
  // classic response
  ///////////////////////////

  console.log(`\n🤖 ${response.choices[0].message.content}\n\n`);
}
