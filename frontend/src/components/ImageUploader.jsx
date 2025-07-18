import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X } from 'lucide-react';

const ImageUploader = ({ onFilesChange, existingImages = [] }) => {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    const initialFiles = existingImages.map(img => ({
      ...img,
      preview: img.url,
    }));
    setFiles(initialFiles);
  }, [existingImages]);

  const onDrop = useCallback(acceptedFiles => {
    const newFiles = acceptedFiles.map(file => Object.assign(file, {
      preview: URL.createObjectURL(file)
    }));
    const updatedFiles = [...files, ...newFiles];
    setFiles(updatedFiles);
    onFilesChange(updatedFiles);
  }, [files, onFilesChange]);

  const removeFile = (fileToRemove) => {
    const updatedFiles = files.filter(file => file !== fileToRemove);
    setFiles(updatedFiles);
    onFilesChange(updatedFiles);
    if (fileToRemove.preview.startsWith('blob:')) {
      URL.revokeObjectURL(fileToRemove.preview);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': [],
      'image/png': [],
      'image/webp': [],
      'image/gif': [],
    },
    maxSize: 5 * 1024 * 1024, // 5MB
  });

  const thumbs = files.map(file => (
    <div className="relative w-24 h-24 border-2 border-muted rounded-lg overflow-hidden" key={file.name || file.id}>
      <img
        src={file.preview}
        alt="Preview"
        className="w-full h-full object-cover"
        onLoad={() => { if (file.preview.startsWith('blob:')) URL.revokeObjectURL(file.preview) }}
      />
      <button
        type="button"
        onClick={() => removeFile(file)}
        className="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1"
      >
        <X className="w-3 h-3" />
      </button>
    </div>
  ));

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`p-6 border-2 border-dashed rounded-lg text-center cursor-pointer transition-colors ${
          isDragActive ? 'border-red-600 bg-red-50 dark:bg-red-900/20' : 'border-muted-foreground/50 hover:border-red-500'
        }`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center space-y-2">
          <Upload className="w-10 h-10 text-muted-foreground" />
          {isDragActive ? (
            <p>Drop the files here ...</p>
          ) : (
            <p>Drag 'n' drop some files here, or click to select files</p>
          )}
          <p className="text-xs text-muted-foreground">PNG, JPG, GIF up to 5MB</p>
        </div>
      </div>
      {files.length > 0 && (
        <aside className="flex flex-wrap gap-4">
          {thumbs}
        </aside>
      )}
    </div>
  );
};

export default ImageUploader;