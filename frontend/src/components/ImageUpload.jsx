import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, Eye, RotateCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/components/ui/use-toast';
import apiService from '@/lib/api';

const ImageUpload = ({ onImagesChange, existingImages = [], maxImages = 10 }) => {
  const [images, setImages] = useState(existingImages);
  const [isUploading, setIsUploading] = useState(false);
  const [previewImage, setPreviewImage] = useState(null);
  const { toast } = useToast();

  const onDrop = useCallback(async (acceptedFiles) => {
    if (images.length + acceptedFiles.length > maxImages) {
      toast({
        title: "Too many images",
        description: `Maximum ${maxImages} images allowed`,
        variant: "destructive",
      });
      return;
    }

    setIsUploading(true);
    
    try {
      const uploadPromises = acceptedFiles.map(async (file) => {
        try {
          // Upload file to backend
          const response = await apiService.uploadFile(file);
          
          if (response.data) {
            return {
              id: Date.now() + Math.random(),
              url: `http://localhost:5000/${response.data.url}`, // Full URL for display
              backendUrl: response.data.url, // Backend relative URL for saving
              name: response.data.filename,
              size: response.data.size,
              type: file.type,
              uploadedAt: new Date().toISOString(),
            };
          }
          throw new Error('Upload failed');
        } catch (error) {
          console.error('Upload error for file:', file.name, error);
          toast({
            title: "Upload failed",
            description: `Failed to upload ${file.name}`,
            variant: "destructive",
          });
          return null;
        }
      });
      
      const uploadResults = await Promise.all(uploadPromises);
      const successfulUploads = uploadResults.filter(result => result !== null);
      
      if (successfulUploads.length > 0) {
        const updatedImages = [...images, ...successfulUploads];
        setImages(updatedImages);
        onImagesChange(updatedImages);
        
        toast({
          title: "Images uploaded",
          description: `${successfulUploads.length} image(s) uploaded successfully`,
        });
      }
      
    } catch (error) {
      console.error('Upload error:', error);
      toast({
        title: "Upload failed",
        description: "Failed to upload images. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  }, [images, maxImages, onImagesChange, toast]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.webp']
    },
    multiple: true,
    disabled: isUploading || images.length >= maxImages
  });

  const removeImage = async (imageId) => {
    const imageToRemove = images.find(img => img.id === imageId);
    
    if (imageToRemove && imageToRemove.backendUrl) {
      try {
        // Delete from backend
        await apiService.deleteFile({ url: imageToRemove.backendUrl });
      } catch (error) {
        console.error('Failed to delete file from backend:', error);
        // Continue with removal from UI even if backend deletion fails
      }
    }
    
    const updatedImages = images.filter(img => img.id !== imageId);
    setImages(updatedImages);
    onImagesChange(updatedImages);
    
    // Clean up preview URL if it exists
    if (imageToRemove && imageToRemove.previewUrl) {
      URL.revokeObjectURL(imageToRemove.previewUrl);
    }
  };

  const moveImage = (fromIndex, toIndex) => {
    const updatedImages = [...images];
    const [movedImage] = updatedImages.splice(fromIndex, 1);
    updatedImages.splice(toIndex, 0, movedImage);
    setImages(updatedImages);
    onImagesChange(updatedImages);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-6">
      {/* Dropzone */}
      <Card className="border-dashed border-2 border-gray-300 hover:border-red-400 transition-colors">
        <CardContent className="p-6">
          <div
            {...getRootProps()}
            className={`cursor-pointer text-center p-8 rounded-lg transition-colors ${
              isDragActive 
                ? 'bg-red-50 border-red-300' 
                : 'hover:bg-gray-50'
            } ${
              isUploading || images.length >= maxImages 
                ? 'opacity-50 cursor-not-allowed' 
                : ''
            }`}
          >
            <input {...getInputProps()} />
            
            <div className="flex flex-col items-center space-y-4">
              {isUploading ? (
                <RotateCw className="w-12 h-12 text-red-500 animate-spin" />
              ) : (
                <Upload className="w-12 h-12 text-gray-400" />
              )}
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {isUploading ? 'Uploading images...' : 'Upload Property Images'}
                </h3>
                <p className="text-gray-500 mt-1">
                  {isDragActive
                    ? 'Drop the images here...'
                    : 'Drag & drop images here, or click to select files'
                  }
                </p>
                <p className="text-sm text-gray-400 mt-2">
                  Supports: JPEG, PNG, GIF, WebP (Max {maxImages} images, 16MB each)
                </p>
              </div>
              
              <Badge variant="outline" className="text-xs">
                {images.length} / {maxImages} images uploaded
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Image Grid */}
      {images.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {images.map((image, index) => (
            <Card key={image.id} className="overflow-hidden group hover:shadow-lg transition-shadow">
              <div className="relative aspect-square">
                <img
                  src={image.url || image.previewUrl}
                  alt={image.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.src = '/placeholder-image.jpg'; // Fallback image
                  }}
                />
                
                {/* Overlay with controls */}
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <div className="flex space-x-2">
                    <Button
                      size="sm"
                      variant="secondary"
                      onClick={() => setPreviewImage(image)}
                      className="bg-white/90 hover:bg-white"
                    >
                      <Eye className="w-4 h-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant="destructive"
                      onClick={() => removeImage(image.id)}
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
                
                {/* Index badge */}
                <Badge className="absolute top-2 left-2 bg-red-600">
                  {index + 1}
                </Badge>
                
                {/* Upload status */}
                {isUploading && (
                  <div className="absolute bottom-2 right-2">
                    <RotateCw className="w-4 h-4 text-white animate-spin" />
                  </div>
                )}
              </div>
              
              <CardContent className="p-3">
                <p className="text-sm font-medium text-gray-900 truncate" title={image.name}>
                  {image.name}
                </p>
                <p className="text-xs text-gray-500">
                  {formatFileSize(image.size)}
                </p>
                {image.backendUrl && (
                  <p className="text-xs text-green-600">
                    ✓ Saved
                  </p>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Image Preview Modal */}
      {previewImage && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="relative max-w-4xl max-h-full">
            <img
              src={previewImage.url || previewImage.previewUrl}
              alt={previewImage.name}
              className="max-w-full max-h-full object-contain"
            />
            
            <Button
              size="sm"
              variant="secondary"
              onClick={() => setPreviewImage(null)}
              className="absolute top-4 right-4 bg-white/90 hover:bg-white"
            >
              <X className="w-4 h-4" />
            </Button>
            
            <div className="absolute bottom-4 left-4 bg-black bg-opacity-75 text-white p-3 rounded-lg">
              <p className="font-medium">{previewImage.name}</p>
              <p className="text-sm opacity-75">{formatFileSize(previewImage.size)}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;