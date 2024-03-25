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
// without streaming
///////////////////////////

while (true) {
  const question = await getUserMessage();

  if (question === 'bye') {
    process.exit();
  }

  context.push({ role: 'user', content: question });

  const response = await openai.chat.completions.create({
    model: 'gpt-4-1106-preview',
    temperature: 0.2,
    messages: context,
  });

  console.log(JSON.stringify(response, null, 2));

  const assistantResponse = response.choices[0].message.content;

  context.push({ role: 'assistant', content: assistantResponse });

  console.log(`\n🤖 ${assistantResponse}\n\n`);
  console.log(response.usage);
}

///////////////////////////
// with streaming
///////////////////////////

// while (true) {
//   const question = await getUserMessage();

//   if (question === 'bye') {
//     process.exit();
//   }

//   context.push({ role: 'user', content: question });

//   const stream = await openai.chat.completions.create({
//     model: 'gpt-4',
//     temperature: 0.2,
//     messages: context,
//     stream: true,
//   });

//   process.stdout.write('\n🤖 ');

//   for await (const chunk of stream) {
//     process.stdout.write(chunk.choices[0]?.delta?.content || '');
//   }

//   console.log('\n\n');
// }
