import React, { useState, useEffect } from 'react'
import { Upload, FileText, Trash2, Eye } from 'lucide-react'
import { uploadDocument, listDocuments, deleteDocument } from '../services/api'

interface Document {
  id: number
  title: string
  source: string
  document_type: string
  created_at: string
}

const DocumentUpload: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      const docs = await listDocuments()
      setDocuments(docs)
    } catch (error) {
      console.error('Failed to load documents:', error)
    }
  }

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    setUploadProgress(0)

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 200)

      await uploadDocument(selectedFile)
      
      clearInterval(progressInterval)
      setUploadProgress(100)
      
      // Reset form and reload documents
      setSelectedFile(null)
      if (event.target instanceof HTMLInputElement) {
        event.target.value = ''
      }
      await loadDocuments()
      
      setTimeout(() => setUploadProgress(0), 1000)
    } catch (error) {
      console.error('Upload failed:', error)
      alert('Upload thất bại. Vui lòng thử lại.')
    } finally {
      setIsUploading(false)
    }
  }

  const handleDelete = async (documentId: number) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa tài liệu này?')) {
      try {
        await deleteDocument(documentId)
        await loadDocuments()
      } catch (error) {
        console.error('Delete failed:', error)
        alert('Xóa thất bại. Vui lòng thử lại.')
      }
    }
  }

  const getFileIcon = (fileType: string) => {
    switch (fileType.toLowerCase()) {
      case 'pdf':
        return '📄'
      case 'txt':
        return '📝'
      case 'md':
        return '📖'
      default:
        return '📁'
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Upload Section */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">
          Upload Tài liệu mới
        </h2>
        
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <input
              type="file"
              accept=".pdf,.txt,.md"
              onChange={handleFileSelect}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              disabled={isUploading}
            />
            <button
              onClick={handleUpload}
              disabled={!selectedFile || isUploading}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              <Upload className="w-4 h-4" />
              <span>{isUploading ? 'Đang upload...' : 'Upload'}</span>
            </button>
          </div>

          {selectedFile && (
            <div className="text-sm text-gray-600">
              File đã chọn: <span className="font-medium">{selectedFile.name}</span>
              <span className="ml-2 text-gray-500">
                ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
              </span>
            </div>
          )}

          {isUploading && (
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
          )}

          <div className="text-sm text-gray-500">
            Hỗ trợ: PDF, TXT, MD (tối đa 10MB)
          </div>
        </div>
      </div>

      {/* Documents List */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-medium text-gray-900">
            Tài liệu đã upload ({documents.length})
          </h2>
        </div>

        <div className="divide-y divide-gray-200">
          {documents.length === 0 ? (
            <div className="px-6 py-8 text-center text-gray-500">
              <FileText className="mx-auto h-12 w-12 text-gray-300 mb-4" />
              <p>Chưa có tài liệu nào được upload</p>
            </div>
          ) : (
            documents.map((doc) => (
              <div key={doc.id} className="px-6 py-4 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getFileIcon(doc.document_type)}</span>
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">{doc.title}</h3>
                    <p className="text-sm text-gray-500">
                      {doc.source} • {new Date(doc.created_at).toLocaleDateString('vi-VN')}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="p-2 text-gray-400 hover:text-red-500 transition-colors"
                    title="Xóa tài liệu"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default DocumentUpload
