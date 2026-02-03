"use client";

import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card } from "@/components/ui/card";
import { Loader2, UploadCloud } from "lucide-react"; // Optional icon
import Filecard from "@/app/components/filecard";

export default function FileUpload() {

    const [files, setFiles] = useState<string[]>([]);
    const [isFetching, setIsFetching] = useState(false);

    // --- FUNCTION TO GET FILES ---
    const fetchFiles = useCallback(async () => {
        setIsFetching(true);
        try {
            const response = await fetch("http://localhost:8000/api/v1/files/list");
            const data = await response.json();
            setFiles(data.files || []); // data.files matches your FastAPI return
        } catch (error) {
            console.error("Error fetching files:", error);
        } finally {
            setIsFetching(false);
        }
    }, []);

    // --- AUTO-FETCH ON PAGE LOAD ---
    useEffect(() => {
        fetchFiles();
    }, [fetchFiles]);


    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        // 1. Initialize FormData
        const formData = new FormData();

        // 2. Append each file. 
        // IMPORTANT: The key "files" must match your FastAPI parameter name
        acceptedFiles.forEach((file) => {
            formData.append("files", file);
        });

        try {
            const response = await fetch("http://localhost:8000/api/v1/files/upload", {
                method: "POST",
                body: formData,
                // Note: Do NOT set Content-Type header. 
                // The browser will set it automatically with the correct boundary.
            });

            if (response.ok) {
                fetchFiles();
                // const data = await response.json();
                // console.log("Upload successful:", data);
                // alert("Files uploaded successfully!");
            } else {
                console.error("Upload failed");
            }
        } catch (error) {
            console.error("Error connecting to server:", error);
        }
    }, [fetchFiles]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        multiple: true,
        accept: { 'application/pdf': [] } // Restrict to images if needed
    });

    return (
        <div>
            <div className="flex flex-col gap-4 max-w-2xl mx-auto p-3">
                <Card
                    {...getRootProps()}
                    className={`
        relative border-2 border-dashed p-12 
        flex flex-col items-center justify-center 
        transition-colors cursor-pointer
        ${isDragActive ? "border-primary bg-secondary/50" : "border-muted-foreground/25"}
      `}
                >
                    <input {...getInputProps()} />
                    <UploadCloud className="h-10 w-10 mb-4 text-muted-foreground" />
                    <p className="text-sm text-muted-foreground">
                        {isDragActive
                            ? "Drop the files here..."
                            : "Drag & drop files here, or click to select"}
                    </p>
                </Card>
            </div>
            <div className="flex flex-col gap-3 max-w-2xl mx-auto p-3">
                <div className="flex items-center justify-between">
                    {/* <h2 className="text-lg font-semibold">Available Files</h2> */}
                    {isFetching && <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />}
                </div>

                {files.length === 0 && !isFetching && (
                    <p className="text-sm text-muted-foreground italic">No files found on server.</p>
                )}

                {files.map((fileName, index) => (
                    <Filecard key={index} name={fileName} />
                ))}
            </div>
        </div>
    );
}