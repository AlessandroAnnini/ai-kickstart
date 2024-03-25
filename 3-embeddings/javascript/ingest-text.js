import { TextLoader } from 'langchain/document_loaders/fs/text';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { OpenAIEmbeddings } from 'langchain/embeddings/openai';
import { HNSWLib } from 'langchain/vectorstores/hnswlib';

///////////////////////////
// Create docs with a loader
///////////////////////////

const loader = new TextLoader('3-embeddings/alice-in-wonderland.txt');

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 2000,
  chunkOverlap: 200,
});

const docs = await loader.loadAndSplit(splitter);

///////////////////////////
// Load the docs into the vector store
///////////////////////////

const vectorStore = await HNSWLib.fromDocuments(
  docs,
  new OpenAIEmbeddings({ openAIApiKey: process.env['OPENAI_API_KEY'] })
);

///////////////////////////
// Save the vector store to a directory
///////////////////////////

const directory = '3-embeddings/v-store';
await vectorStore.save(directory);
