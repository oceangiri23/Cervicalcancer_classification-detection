import {useState} from "react";
import "./App.css";
import ModeSelector from "./components/ModeSelector";
import ImageUpload from "./components/ImageUpload";
import AnalysisResult from "./components/AnalysisResult";

export default function App() {
  const [selectedMode, setSelectedMode] = useState("classification");
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleModeChange = (mode) => {
    setSelectedMode(mode);
    // Reset results when mode changes
    setResult(null);
    setError(null);
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type.startsWith("image/")) {
        setSelectedFile(file);
        setError(null);
        setResult(null);

        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
          setImagePreview(e.target.result);
        };
        reader.readAsDataURL(file);
      } else {
        setError("Please select a valid image file");
      }
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setError("Please select an image file");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("image", selectedFile);

      // Add detection parameter when detection mode is selected
      if (selectedMode === "detection") {
        formData.append("is_detection", "true");
      }

      const response = await fetch("http://localhost:8000/process-image", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process image");
      }

      const data = await response.json();
      console.log("Response data:", data);

      setResult(data);
    } catch (err) {
      setError(err.message || "An error occurred while processing the image");
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setImagePreview(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold text-gray-900">
            Cervical Cancer Detection System
          </h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="space-y-8">
          <ModeSelector
            selectedMode={selectedMode}
            onModeChange={handleModeChange}
          />

          <ImageUpload
            selectedFile={selectedFile}
            imagePreview={imagePreview}
            isLoading={isLoading}
            error={error}
            selectedMode={selectedMode}
            onFileUpload={handleFileUpload}
            onSubmit={handleSubmit}
            onReset={resetForm}
          />

          {result && (
            <AnalysisResult
              result={result}
              selectedFile={selectedFile}
              selectedMode={selectedMode}
            />
          )}
        </div>
      </main>
    </div>
  );
}
