import { Link } from "react-router-dom";
import { ArrowRight, Sparkles, ShieldCheck, TrendingUp, Hotel } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-hero-gradient relative overflow-hidden">
      <div className="absolute top-20 left-1/4 w-96 h-96 bg-primary-300/25 rounded-full blur-3xl animate-float" />
      <div className="absolute bottom-10 right-1/4 w-96 h-96 bg-accent-400/20 rounded-full blur-3xl animate-float" style={{ animationDelay: "2s" }} />

      <div className="relative max-w-5xl mx-auto px-6 pt-24 pb-20 text-center animate-fade-in">
        <div className="inline-flex items-center gap-1.5 bg-white/70 backdrop-blur border border-white text-primary-700 text-xs font-semibold px-4 py-1.5 rounded-full mb-6 shadow-sm">
          <Sparkles className="w-3.5 h-3.5" />
          Powered by Machine Learning
        </div>

        <h1 className="font-display font-extrabold text-4xl sm:text-6xl text-gray-900 leading-tight">
          Smarter stays,
          <br />
          <span className="brand-text">smarter pricing.</span>
        </h1>

        <p className="text-gray-500 text-lg mt-6 max-w-xl mx-auto">
          LuxeStay uses real-time AI to predict fair prices and flag booking
          risks — so you always know exactly what you're getting.
        </p>

        <div className="flex items-center justify-center gap-4 mt-10">
          <Link
            to={isAuthenticated ? "/rooms" : "/register"}
            className="flex items-center gap-2 bg-brand-gradient text-white font-semibold px-7 py-3.5 rounded-full shadow-glow hover:opacity-90 transition-opacity"
          >
            Explore Rooms <ArrowRight className="w-4 h-4" />
          </Link>
          {!isAuthenticated && (
            <Link
              to="/login"
              className="px-7 py-3.5 rounded-full font-semibold text-gray-700 bg-white/70 backdrop-blur border border-white hover:bg-white transition-colors"
            >
              Sign In
            </Link>
          )}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-24 text-left">
          {[
            {
              icon: TrendingUp,
              title: "Dynamic Pricing",
              desc: "Prices adapt in real time to season, demand, and stay length using a trained ML model.",
            },
            {
              icon: ShieldCheck,
              title: "Cancellation Insights",
              desc: "Every booking gets a live cancellation-risk score so the hotel can plan smarter.",
            },
            {
              icon: Hotel,
              title: "Seamless Booking",
              desc: "Browse rooms, book instantly, and manage everything from one clean dashboard.",
            },
          ].map((f, i) => (
            <div
              key={f.title}
              className="glass-card rounded-2xl p-6 shadow-card animate-slide-up"
              style={{ animationDelay: `${i * 100}ms` }}
            >
              <div className="w-11 h-11 rounded-xl bg-brand-gradient flex items-center justify-center mb-4 shadow-glow">
                <f.icon className="w-5 h-5 text-white" />
              </div>
              <h3 className="font-display font-semibold text-gray-900 mb-1.5">
                {f.title}
              </h3>
              <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
