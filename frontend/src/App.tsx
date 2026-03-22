import React from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';

export default function App() {
  return (
    <div className="bg-warm-sand min-h-screen font-sans flex items-center justify-center p-4">
      <div className="bg-soft-blush relative overflow-hidden max-w-[400px] w-full min-h-[820px] rounded-[40px] shadow-soft flex flex-col isolation-auto">
        
        {/* Organic Background Blobs */}
        <div className="absolute top-[-5%] right-[-15%] w-[250px] h-[250px] bg-white opacity-40 organic-blob pointer-events-none -z-10 blur-xl"></div>
        <div className="absolute top-[30%] left-[-20%] w-[300px] h-[300px] bg-primary-rose opacity-10 organic-blob pointer-events-none -z-10 blur-2xl"></div>
        
        {/* Top Header */}
        <div className="flex justify-between items-center p-6 pt-10">
          <div className="flex items-center gap-2">
            <div className="bg-deep-maroon p-[6px] rounded-full shadow-sm">
               <Sparkles size={14} className="text-soft-blush" />
            </div>
            <span className="font-display font-bold text-deep-maroon text-lg tracking-tight">RoomAI</span>
          </div>
          <button className="text-deep-maroon/60 font-medium text-sm hover:text-deep-maroon transition-colors py-2 px-3">Skip</button>
        </div>

        {/* Hero Image Area */}
        <div className="flex-1 w-full flex items-center justify-center px-6 pb-2 z-10 relative mt-2">
          <div className="relative w-full aspect-[4/5] rounded-[32px] overflow-hidden shadow-soft border-4 border-white/40">
            <img 
              src="https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&q=80&w=800" 
              alt="Beautiful interior design" 
              className="object-cover w-full h-full scale-105 hover:scale-110 transition-transform duration-700 ease-in-out"
            />
            {/* Soft inner vignette overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-deep-maroon/30 to-transparent mix-blend-multiply"></div>
            
            {/* Pill overlay badge */}
            <div className="absolute bottom-5 left-5 bg-white/90 backdrop-blur-md px-4 py-2 rounded-full shadow-sm flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-primary-rose"></span>
              <span className="text-[11px] font-bold text-deep-maroon uppercase tracking-wider">Organic Velvet</span>
            </div>
          </div>
        </div>

        {/* Bottom Content Area */}
        <div className="bg-white rounded-[40px] p-8 pt-10 z-10 flex flex-col gap-6 shadow-[0_-15px_40px_rgba(206,107,127,0.08)] mt-auto mx-2 mb-2 relative">
          <div className="flex flex-col gap-3">
            <h1 className="font-display text-[2.2rem] leading-[1.1] font-bold text-deep-maroon tracking-tight">
              Design your<br/>dream space.
            </h1>
            <p className="text-deep-maroon/60 text-[15px] leading-relaxed font-medium pr-4">
              Transform any room with AI-powered interior design. Discover your perfect aesthetic in seconds.
            </p>
          </div>

          <button className="w-full bg-primary-rose hover:bg-opacity-90 hover:shadow-[0_12px_28px_rgba(206,107,127,0.4)] transition-all text-white font-semibold py-[18px] rounded-full shadow-rose mt-2 flex items-center justify-center gap-2 text-[17px] group">
            Get Started
            <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
          </button>
          
          {/* Pagination dots */}
          <div className="flex justify-center items-center gap-2 mt-2">
            <span className="w-8 h-[6px] rounded-full bg-primary-rose"></span>
            <span className="w-[6px] h-[6px] rounded-full bg-warm-sand"></span>
            <span className="w-[6px] h-[6px] rounded-full bg-warm-sand"></span>
          </div>
        </div>

      </div>
    </div>
  );
}
