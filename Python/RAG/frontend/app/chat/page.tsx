'use client';

import { useState, useEffect, Fragment } from 'react';
import { RefreshCcwIcon, CopyIcon, GlobeIcon } from 'lucide-react';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';

import {
  Item,
  ItemContent,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item"
import {
  MessageActions,
  MessageAction,
  Message,
  MessageContent,
  MessageResponse
} from '@/components/ai-elements/message';
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from '@/components/ai-elements/conversation';
import {
  PromptInput,
  PromptInputActionAddAttachments,
  PromptInputActionMenu,
  PromptInputActionMenuContent,
  PromptInputActionMenuTrigger,
  PromptInputBody,
  PromptInputButton,
  PromptInputHeader,
  PromptInputSelect,
  PromptInputSelectContent,
  PromptInputSelectItem,
  PromptInputSelectTrigger,
  PromptInputSelectValue,
  PromptInputSubmit,
  PromptInputTextarea,
  PromptInputFooter,
  PromptInputTools,
  usePromptInputAttachments,
} from '@/components/ai-elements/prompt-input';
import { Spinner } from "@/components/ui/spinner"


// --- 3. DATA & UTILS ---
import { fetchOllamaModels } from "@/lib/api-helpers";

// get ollama models using an api
// Todo: idea is to use this api to select available model for the llm
// const models = await fetchOllamaModels() || {};


// --- 5. MAIN COMPONENT ---

const ActionsDemo = () => {
  // --- STATE ---
  // const [model, setModel] = useState<string>(models[0]?.["model"] || "");
  const [input, setInput] = useState('');

  // --- CHAT HOOK ---
  const { messages, sendMessage, status, regenerate, stop } = useChat({
    transport: new DefaultChatTransport({
      api: 'http://localhost:8000/api/v1/chat',
    }),
  });

  // --- HANDLERS ---
  const handleSubmit = (_message: any, e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (input.trim()) {
      sendMessage({ text: input });
      setInput('');
    }
  };

  return (

    <div className="flex flex-col h-[calc(100vh-3.5rem)] max-w-4xl mx-auto w-full bg-white ">

      {/* --- CONVERSATION AREA --- */}
      <Conversation className='flex-1 h-lvh p-4 space-y-4'>

        <ConversationContent>
          {messages.map((message, messageIndex) => (
            <Fragment key={message.id}>
              {message.parts.map((part, i) => {
                switch (part.type) {
                  case 'text':
                    const isLastMessage = messageIndex === messages.length - 1;
                    return (
                      <Fragment key={`${message.id}-${i}`}>
                        <Message from={message.role}>
                          <MessageContent>
                            {message.role === 'assistant' && isLastMessage && status === 'streaming' && (
                              <Item variant="muted">
                                <ItemMedia>
                                  <Spinner />
                                </ItemMedia>
                                <ItemContent>
                                  <ItemTitle className="line-clamp-1">Generating response...</ItemTitle>
                                </ItemContent>
                              </Item>

                            )}
                            <MessageResponse>
                              {part.text}
                            </MessageResponse>
                            {/* {status === 'streaming' &&()} */}
                          </MessageContent>
                        </Message>

                        {/* Action buttons for Assistant's last response */}
                        {message.role === 'assistant' && isLastMessage && (
                          <MessageActions>

                            <MessageAction
                              onClick={() => regenerate()}
                              label="Retry"
                            >
                              <RefreshCcwIcon className="size-3" />
                            </MessageAction>
                            <MessageAction
                              onClick={() => navigator.clipboard.writeText(part.text)}
                              label="Copy"
                            >
                              <CopyIcon className="size-3" />
                            </MessageAction>
                          </MessageActions>
                        )}
                      </Fragment>
                    );
                  default:
                    return null;
                }
              })}
            </Fragment>
          ))}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>

      {/* --- INPUT AREA --- */}
      <div className="p-4 bg-background">
        <PromptInput
          onSubmit={handleSubmit}
          className="mt-4 w-full p-2 relative"
        >

          {/* Middle: Text Box */}
          <PromptInputBody>
            <PromptInputTextarea
              value={input}
              placeholder="Say something..."
              onChange={(e) => setInput(e.currentTarget.value)}
              className="pr-12"
            />
          </PromptInputBody>

          {/* Bottom: Toolbar Actions */}
          <PromptInputFooter>
            <PromptInputTools>

              {/* Model Selector */}
              {/* <PromptInputSelect
                onValueChange={(value) => setModel(value)}
                value={model}
              >
                <PromptInputSelectTrigger>
                  <PromptInputSelectValue />
                </PromptInputSelectTrigger>
                <PromptInputSelectContent>
                  {models.map((model: any) => (
                    <PromptInputSelectItem key={model.model} value={model.model}>
                      {model.model}{model.parameter_size}
                    </PromptInputSelectItem>
                  ))}
                </PromptInputSelectContent>
              </PromptInputSelect> */}
            </PromptInputTools>

            {/* Submit Button */}
            {/* <PromptInputSubmit
              status={status === 'streaming' ? 'streaming' : 'ready'}
              disabled={!input.trim()}
              className="absolute bottom-1 right-1"
            /> */}

            {/* --- SUBMIT / STOP BUTTON --- */}
            {status === 'streaming' ? (
              <PromptInputButton
                onClick={() => stop()}
                variant="destructive"
                className="absolute bottom-1 right-1 size-8 p-0"
              >
                {/* Square icon representing 'Stop' */}
                <div className="size-3 bg-white rounded-sm" />
              </PromptInputButton>
            ) : (
              <PromptInputSubmit
                status="ready"
                disabled={!input.trim()}
                className="absolute bottom-1 right-1"
              />
            )}
          </PromptInputFooter>
        </PromptInput>
      </div>

    </div>

  );
};

export default ActionsDemo;


























// 'use client';
// import { useState, useEffect } from 'react';
// import { MessageActions, MessageAction } from '@/components/ai-elements/message';
// import { Message, MessageContent } from '@/components/ai-elements/message';
// import { DefaultChatTransport } from 'ai';
// import {
//   Conversation,
//   ConversationContent,
//   ConversationScrollButton,
// } from '@/components/ai-elements/conversation';
// import {
//   PromptInput,
//   PromptInputActionAddAttachments,
//   PromptInputActionMenu,
//   PromptInputActionMenuContent,
//   PromptInputActionMenuTrigger,
//   PromptInputBody,
//   PromptInputButton,
//   PromptInputHeader,
//   type PromptInputMessage,
//   PromptInputSelect,
//   PromptInputSelectContent,
//   PromptInputSelectItem,
//   PromptInputSelectTrigger,
//   PromptInputSelectValue,
//   PromptInputSubmit,
//   PromptInputTextarea,
//   PromptInputFooter,
//   PromptInputTools,
//   usePromptInputAttachments,
// } from '@/components/ai-elements/prompt-input';
// import { MessageResponse } from '@/components/ai-elements/message';
// import { RefreshCcwIcon, CopyIcon } from 'lucide-react';
// import { useChat } from '@ai-sdk/react';
// import { Fragment } from 'react';

// import {
//   Attachment,
//   AttachmentPreview,
//   AttachmentRemove,
//   Attachments,
// } from '@/components/ai-elements/attachments';
// import { GlobeIcon } from 'lucide-react';
// import { fetchOllamaModels } from "@/lib/api-helpers";


// const models = await fetchOllamaModels() || {};
// // console.log(models[0]["model"])

// // handle attachments
// const PromptInputAttachmentsDisplay = () => {
//   const attachments = usePromptInputAttachments();

//   if (attachments.files.length === 0) {
//     return null;
//   }

//   return (
//     <Attachments variant="inline">
//       {attachments.files.map((attachment) => (
//         <Attachment
//           data={attachment}
//           key={attachment.id}
//           onRemove={() => attachments.remove(attachment.id)}
//         >
//           <AttachmentPreview />
//           <AttachmentRemove />
//         </Attachment>
//       ))}
//     </Attachments>
//   );
// };


// const ActionsDemo = () => {
//   const [useWebSearch, setUseWebSearch] = useState<boolean>(false);


//   const [model, setModel] = useState<string>(models[0]["model"] || "");

//   const [input, setInput] = useState('');
//   const { messages, sendMessage, status, regenerate, stop } = useChat(
//     {
//       transport: new DefaultChatTransport({
//         api: 'http://localhost:8000/api/v1/chat',
//       }),
//     });
//   const handleSubmit = (_message: any, e: React.FormEvent<HTMLFormElement>) => {
//     e.preventDefault();
//     if (input.trim()) {
//       sendMessage({ text: input });
//       setInput('');
//     }
//   };
//   return (
//     <div className="max-w-6xl mx-auto p-6 relative size-full rounded-lg h-lvh ">
//       <div className="flex flex-col h-full ">
//         <Conversation>
//           <ConversationContent>
//             {messages.map((message, messageIndex) => (
//               <Fragment key={message.id}>
//                 {message.parts.map((part, i) => {
//                   switch (part.type) {
//                     case 'text':
//                       const isLastMessage =
//                         messageIndex === messages.length - 1;
//                       return (
//                         <Fragment key={`${message.id}-${i}`}>
//                           <Message from={message.role}>
//                             <MessageContent>
//                               <MessageResponse>{part.text}</MessageResponse>
//                             </MessageContent>
//                           </Message>
//                           {message.role === 'assistant' && isLastMessage && (
//                             <MessageActions>
//                               <MessageAction
//                                 onClick={() => regenerate()}
//                                 label="Retry"
//                               >
//                                 <RefreshCcwIcon className="size-3" />
//                               </MessageAction>
//                               <MessageAction
//                                 onClick={() =>
//                                   navigator.clipboard.writeText(part.text)
//                                 }
//                                 label="Copy"
//                               >
//                                 <CopyIcon className="size-3" />
//                               </MessageAction>
//                             </MessageActions>
//                           )}
//                         </Fragment>
//                       );
//                     default:
//                       return null;
//                   }
//                 })}
//               </Fragment>
//             ))}
//           </ConversationContent>
//           <ConversationScrollButton />
//         </Conversation>
//         <PromptInput
//           onSubmit={handleSubmit}
//           className="mt-4 w-full max-w-2xl mx-auto relative"
//         >
//           <PromptInputHeader>
//             <PromptInputAttachmentsDisplay />
//           </PromptInputHeader>
//           <PromptInputBody>

//             <PromptInputTextarea
//               value={input}
//               placeholder="Say something..."
//               onChange={(e) => setInput(e.currentTarget.value)}
//               className="pr-12"
//             />
//           </PromptInputBody>

//           <PromptInputFooter>
//             <PromptInputTools>
//               <PromptInputActionMenu>
//                 <PromptInputActionMenuTrigger />
//                 <PromptInputActionMenuContent>
//                   <PromptInputActionAddAttachments />
//                 </PromptInputActionMenuContent>
//               </PromptInputActionMenu>
//               <PromptInputButton
//                 onClick={() => setUseWebSearch(!useWebSearch)}
//                 variant={useWebSearch ? 'default' : 'ghost'}
//               >
//                 <GlobeIcon size={16} />
//                 <span>Search</span>
//               </PromptInputButton>
//               <PromptInputSelect
//                 onValueChange={(value) => {
//                   setModel(value);
//                 }}
//                 value={model}
//               >
//                 <PromptInputSelectTrigger>
//                   <PromptInputSelectValue />
//                 </PromptInputSelectTrigger>
//                 <PromptInputSelectContent>
//                   {models.map((model: any) => (
//                     <PromptInputSelectItem key={model.model} value={model.model}>
//                       {model.model}{model.parameter_size}
//                     </PromptInputSelectItem>
//                   ))}
//                 </PromptInputSelectContent>
//               </PromptInputSelect>
//             </PromptInputTools>
//             <PromptInputSubmit
//               status={status === 'streaming' ? 'streaming' : 'ready'}
//               disabled={!input.trim()}
//               className="absolute bottom-1 right-1"
//             />
//           </PromptInputFooter>

//         </PromptInput>
//       </div>
//     </div>
//   );
// };
// export default ActionsDemo;















































// "use client";

// import { useChat } from '@ai-sdk/react';
// import { useState } from 'react';
// import { DefaultChatTransport } from 'ai';
// import { Streamdown } from 'streamdown';
// import { code } from '@streamdown/code';
// import { mermaid } from '@streamdown/mermaid';
// import { math } from '@streamdown/math';
// import ReactMarkdown from 'react-markdown';
// import remarkGfm from 'remark-gfm';
// import {
//   Conversation,
//   ConversationContent,
//   ConversationScrollButton,
// } from '@/components/ai-elements/conversation';
// import { Message, MessageContent, MessageResponse } from '@/components/ai-elements/message';

// export default function ChatApp() {
//   // 1. You must manage your own input state now (AI SDK 5.0+ requirement)
//   const [input, setInput] = useState('');

//   // 2. Setup useChat with the new Transport architecture
//   const { messages, sendMessage, status } = useChat({
//     transport: new DefaultChatTransport({
//       api: 'http://localhost:8000/chat',
//     }),
//   });
//   console.log("status:", status)
//   console.log("message:", messages)
//   // console.log("messages: " + JSON.stringify(messages, null, 2))
//   // console.table(messages)
//   const handleFormSubmit = (e: React.FormEvent) => {
//     e.preventDefault();
//     if (!input.trim()) return;
//     sendMessage({ text: input });
//     setInput('');
//   };

//   return (
//     <div className="max-w-4xl mx-auto p-6 relative size-full rounded-lg border h-[600px]">
//       <div className="flex flex-col h-full">
//         {messages.map((m) => (
//           <div
//             key={m.id}
//             className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'
//               }`}
//           >
//             <div
//               className={`rounded-2xl px-5 py-4 max-w-max shadow-lg
// dark:border-slate-800'
//                 }`}
//             >
//               {m.parts.map((part, i) => {
//                 if (part.type === 'text') {
//                   return (
//                     <article
//                       key={i}
//                       className={`prose prose-blue prose-sm sm:prose-base max-w-none
//                 prose-code:px-1 prose-code:py-0.4
//                 prose-code:rounded-md
//                 prose-a:underline-offset-4`}
//                     >
//                       <Message from={m.role} >
//                         <MessageContent>
//                           <MessageResponse >
//                             {part.text}
//                           </MessageResponse>
//                         </MessageContent>
//                       </Message>
//                     </article>
//                   );
//                 }
//                 return null;
//               })}
//             </div>
//           </div>
//         ))}

//         {status === 'streaming' && (
//           <div className="text-sm text-slate-400 italic">
//             AI is thinking…
//           </div>
//         )}
//       </div>
//       <form
//         onSubmit={handleFormSubmit}
//         className="fixed bottom-6 left-1/2 -translate-x-1/2 w-full max-w-2xl px-4"
//       >
//         <div className="flex items-center gap-2 rounded-2xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-lg">
//           <input
//             className="flex-1 bg-transparent px-4 py-3 outline-none text-slate-900 dark:text-white placeholder:text-slate-400"
//             value={input}
//             placeholder="Ask the AI anything…"
//             onChange={(e) => setInput(e.target.value)}
//           />
//           <button
//             type="submit"
//             className="mr-2 rounded-xl bg-blue-600 px-4 py-2 text-white font-medium hover:bg-blue-700 transition"
//           >
//             Send
//           </button>
//         </div>
//       </form>

//     </div>
//   );
// }


