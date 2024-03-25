import { ChatOpenAI } from 'langchain/chat_models/openai';
import { OpenAIEmbeddings } from 'langchain/embeddings/openai';
import { HNSWLib } from 'langchain/vectorstores/hnswlib';
import { PromptTemplate } from 'langchain/prompts';
import {
  RunnableSequence,
  RunnablePassthrough,
} from 'langchain/schema/runnable';
import { StringOutputParser } from 'langchain/schema/output_parser';
import { formatDocumentsAsString } from 'langchain/util/document';

///////////////////////////
// Initialize the LLM to use to answer the question
///////////////////////////

const model = new ChatOpenAI({
  openAIApiKey: process.env['OPENAI_API_KEY'],
});

///////////////////////////
// Load the vector store from a directory
///////////////////////////

const directory = '3-embeddings/v-store';
const vectorStore = await HNSWLib.load(directory, new OpenAIEmbeddings());

///////////////////////////
// Create a retriever from the vector store
///////////////////////////

const retriever = vectorStore.asRetriever({ k: 2 });

///////////////////////////
// Create a prompt template
///////////////////////////

const prompt =
  PromptTemplate.fromTemplate(`Answer the question based only on the following context:
{context}

Question: {question}`);

///////////////////////////
// Create a runnable sequence
///////////////////////////

const chain = RunnableSequence.from([
  {
    context: retriever.pipe(formatDocumentsAsString),
    question: new RunnablePassthrough(),
  },
  prompt,
  model,
  new StringOutputParser(),
]);

///////////////////////////
// Invoke the chain
///////////////////////////

const result = await chain.invoke('Who is Alice?');

console.log(result);
