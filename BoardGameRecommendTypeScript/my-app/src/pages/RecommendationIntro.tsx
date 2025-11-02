import { useNavigate } from "react-router-dom";

export default function RecommendationIntro() {
  const navigate = useNavigate();

  return (
    <div
      className="flex flex-col items-center justify-center min-h-screen 
                  bg-gradient-to-br from-green-100 via-yellow-100 to-orange-100 p-6"
    >
      {/* Card Container */}
      <div className="bg-white bg-opacity-90 shadow-xl rounded-2xl p-10 max-w-3xl text-center">
        {/* Title */}
        <h1 className="text-5xl sm:text-6xl font-extrabold text-gray-800 mb-6">
          Game Recommendations
        </h1>

        {/* Description */}
        <p className="text-xl sm:text-2xl leading-relaxed text-gray-700 mb-10">
          Looking for your next favorite board game? Choose your path below —
          either a quick classic quiz or an epic story adventure!
        </p>

        {/* Quiz Options */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Classic Quiz */}
          <button
            onClick={() => navigate("/recommend")}
            className="group bg-blue-600 text-white px-6 py-8 rounded-xl shadow-lg hover:bg-blue-700 transition duration-300"
          >
            <h2 className="text-2xl font-bold mb-2">🎲 Classic Quiz</h2>
            <p className="text-base text-blue-100 group-hover:text-white transition">
              Answer a few quick questions to find your perfect game.
            </p>
          </button>

          {/* Adventure Quiz */}
          <button
            onClick={() => navigate("/adventure")}
            className="group bg-purple-600 text-white px-6 py-8 rounded-xl shadow-lg hover:bg-purple-700 transition duration-300"
          >
            <h2 className="text-2xl font-bold mb-2">🐉 Adventure Quiz</h2>
            <p className="text-base text-purple-100 group-hover:text-white transition">
              Embark on a choose-your-own-story journey to uncover your game
              destiny.
            </p>
          </button>
        </div>
      </div>
    </div>
  );
}
