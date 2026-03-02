import Link from "next/link";
import { ArrowRight, BrainCircuit, TrendingUp, Shield } from "lucide-react";

export default function Hero() {
  return (
    <section className="relative overflow-hidden pt-32 pb-20 lg:pt-40 lg:pb-32">
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-20 left-1/4 h-72 w-72 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute bottom-20 right-1/4 h-96 w-96 rounded-full bg-accent/5 blur-3xl" />
      </div>

      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary">
            <BrainCircuit className="h-4 w-4" />
            ML-Powered Loan Prediction
          </div>

          <h1 className="font-serif text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl text-balance">
            Smart Loan Approval Predictions
          </h1>

          <p className="mt-6 text-lg leading-relaxed text-muted-foreground text-pretty">
            Leverage advanced machine learning algorithms to predict loan
            approval outcomes. Our system analyzes 18+ financial parameters
            using Logistic Regression and KNN models, achieving 86.5% accuracy.
          </p>

          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              href="/predict"
              className="inline-flex items-center gap-2 rounded-lg bg-primary px-8 py-3.5 text-base font-semibold text-primary-foreground shadow-lg transition-all hover:bg-primary/90 hover:shadow-xl"
            >
              Check Eligibility
              <ArrowRight className="h-5 w-5" />
            </Link>
            <Link
              href="#how-it-works"
              className="inline-flex items-center gap-2 rounded-lg border border-border bg-card px-8 py-3.5 text-base font-semibold text-foreground transition-colors hover:bg-secondary"
            >
              Learn More
            </Link>
          </div>
        </div>

        <div className="mx-auto mt-20 grid max-w-4xl grid-cols-1 gap-6 sm:grid-cols-3">
          <div className="flex flex-col items-center gap-3 rounded-xl border border-border bg-card p-6 text-center shadow-sm">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
              <TrendingUp className="h-6 w-6 text-primary" />
            </div>
            <div className="text-2xl font-bold text-foreground font-serif">86.5%</div>
            <p className="text-sm text-muted-foreground">Model Accuracy</p>
          </div>
          <div className="flex flex-col items-center gap-3 rounded-xl border border-border bg-card p-6 text-center shadow-sm">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
              <BrainCircuit className="h-6 w-6 text-primary" />
            </div>
            <div className="text-2xl font-bold text-foreground font-serif">18+</div>
            <p className="text-sm text-muted-foreground">Parameters Analyzed</p>
          </div>
          <div className="flex flex-col items-center gap-3 rounded-xl border border-border bg-card p-6 text-center shadow-sm">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
              <Shield className="h-6 w-6 text-primary" />
            </div>
            <div className="text-2xl font-bold text-foreground font-serif">2</div>
            <p className="text-sm text-muted-foreground">ML Models</p>
          </div>
        </div>
      </div>
    </section>
  );
}
