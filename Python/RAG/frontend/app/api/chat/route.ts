// import { streamText, UIMessage, convertToModelMessages } from 'ai';

// // Allow streaming responses up to 30 seconds
// export const maxDuration = 30;

// export async function POST(req: Request) {
//   const { messages }: { messages: UIMessage[] } = await req.json();

//   const result = streamText({
//     // model: "anthropic/claude-sonnet-4.5",
//     model: "http://127.0.0.1:8000/chat",
//     messages: await convertToModelMessages(messages),
//   });

//   return result.toTextStreamResponse();
// }