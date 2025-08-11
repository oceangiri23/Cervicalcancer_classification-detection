export default function AnalysisResult({result, selectedMode}) {
  const getResultColor = (label) => {
    const colors = {
      Dyskeratotic: "text-red-600",
      Koilocytotic: "text-orange-600",
      Metaplastic: "text-yellow-600",
      Parabasal: "text-blue-600",
      "Superficial-Intermediate": "text-green-600",
    };
    return colors[label] || "text-gray-600";
  };

  const getResultBgColor = (label) => {
    const colors = {
      Dyskeratotic: "bg-red-50 border-red-200",
      Koilocytotic: "bg-orange-50 border-orange-200",
      Metaplastic: "bg-yellow-50 border-yellow-200",
      Parabasal: "bg-blue-50 border-blue-200",
      "Superficial-Intermediate": "bg-green-50 border-green-200",
    };
    return colors[label] || "bg-gray-50 border-gray-200";
  };

  const getCellDescription = (label) => {
    const descriptions = {
      Dyskeratotic:
        "Dyskeratotic cells show abnormal keratinization and may indicate cellular changes that require further medical evaluation.",
      Koilocytotic:
        "Koilocytotic cells show perinuclear clearing and may be associated with HPV infection. They require careful monitoring and follow-up.",
      Metaplastic:
        "Metaplastic cells are immature squamous cells from the transformation zone. They represent normal cellular changes but should be monitored.",
      Parabasal:
        "Parabasal cells are normal immature squamous cells from deeper epithelial layers. They are part of the normal cellular composition.",
      "Superficial-Intermediate":
        "Superficial-Intermediate cells are mature squamous cells from the surface layers. They represent normal, healthy cellular composition.",
    };
    return descriptions[label] || "Cell type information not available.";
  };

  // Render detection result
  if (selectedMode === "detection") {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Detection Results</h2>

        <div className="space-y-6">
          <div>
            <h3 className="text-md font-medium mb-3">Processed Image</h3>
            <div className="border rounded-lg overflow-hidden">
              <img
                src={result.image_url}
                alt="Detection result"
                className="w-full max-h-96 object-contain"
              />
            </div>
          </div>

          {result.detections && result.detections.length > 0 && (
            <div>
              <h3 className="text-md font-medium mb-3">Detected Cells</h3>
              <div className="grid gap-3">
                {result.detections.map((detection, index) => (
                  <div
                    key={index}
                    className={`p-3 rounded-lg border ${getResultBgColor(
                      detection.label
                    )}`}
                  >
                    <div className="flex justify-between items-center">
                      <span
                        className={`font-medium ${getResultColor(
                          detection.label
                        )}`}
                      >
                        {detection.label}
                      </span>
                      <span className="text-sm text-gray-600">
                        Confidence: {(detection.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Render classification result (existing code)
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4">Analysis Results</h2>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Classification Result */}
        <div>
          <h3 className="text-md font-medium mb-3">Classification</h3>
          <div
            className={`p-4 rounded-lg border ${getResultBgColor(
              result.predicted_label
            )}`}
          >
            <div className="text-center">
              <div
                className={`text-xl font-bold mb-2 ${getResultColor(
                  result.predicted_label
                )}`}
              >
                {result.predicted_label}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Cell Information */}
      <div className="mt-6">
        <h3 className="text-md font-medium mb-3">Cell Type Information</h3>
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <h4 className="font-medium text-blue-900 mb-2">
            About {result.predicted_label} Cells:
          </h4>
          <p className="text-sm text-blue-800 leading-relaxed">
            {getCellDescription(result.predicted_label)}
          </p>
        </div>
      </div>
    </div>
  );
}
