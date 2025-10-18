import { useNavigate } from "react-router-dom";

export default function RecommendationIntro() {
  const navigate = useNavigate();

  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen 
                    bg-gradient-to-br from-green-100 via-yellow-100 to-orange-100 p-6"
    >
      {/* Card Container */}
      <div className="bg-white bg-opacity-90 shadow-xl rounded-2xl p-10 max-w-2xl text-center">
        {/* Title */}
        <h1 className="text-5xl sm:text-6xl font-extrabold text-gray-800 mb-6">
          Game Recommendations
        </h1>

        {/* Description */}
        <p className="text-xl sm:text-2xl leading-relaxed text-gray-700 mb-10">
          Looking for a new game to spice up your game night? Answer a few
          questions and you'll get a personalized game recommendation in
          moments.
        </p>

        {/* Start Button */}
        <button
          onClick={() => navigate("/recommend")}
          className="px-8 py-3 bg-blue-600 text-white text-lg rounded-lg shadow-lg hover:bg-blue-700 transition duration-300"
        >
          Start Recommendation
        </button>
      </div>
    </div>
  );
}
