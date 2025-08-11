export default function ModeSelector({selectedMode, onModeChange}) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4">Analysis Mode</h2>
      <div className="grid grid-cols-2 gap-4">
        <button
          onClick={() => onModeChange("classification")}
          className={`p-4 rounded-lg border-2 transition-colors ${
            selectedMode === "classification"
              ? "border-blue-500 bg-blue-50 text-blue-700"
              : "border-gray-200 hover:border-blue-300"
          }`}
        >
          <div className="text-center">
            <h3 className="font-medium mb-2">Classification</h3>
            <p className="text-sm text-gray-600">
              Classify cell types in cervical images
            </p>
          </div>
        </button>

        <button
          onClick={() => onModeChange("detection")}
          className={`p-4 rounded-lg border-2 transition-colors ${
            selectedMode === "detection"
              ? "border-blue-500 bg-blue-50 text-blue-700"
              : "border-gray-200 hover:border-blue-300"
          }`}
        >
          <div className="text-center">
            <h3 className="font-medium mb-2">Detection</h3>
            <p className="text-sm text-gray-600">
              Detect cervical abnormalities in images
            </p>
          </div>
        </button>
      </div>
    </div>
  );
}
