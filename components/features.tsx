import {
  Wallet,
  UserCheck,
  BarChart3,
  Building,
  CreditCard,
  PieChart,
} from "lucide-react";

const features = [
  {
    icon: Wallet,
    title: "Income Analysis",
    description:
      "Evaluates applicant and co-applicant income to assess repayment capacity and financial stability.",
  },
  {
    icon: CreditCard,
    title: "Credit Assessment",
    description:
      "Analyzes credit score, existing loans, and DTI ratio to gauge creditworthiness and risk level.",
  },
  {
    icon: UserCheck,
    title: "Profile Evaluation",
    description:
      "Considers age, education, employment status, and personal details for a comprehensive applicant profile.",
  },
  {
    icon: Building,
    title: "Property & Collateral",
    description:
      "Assesses property area, collateral value, and employer category to determine loan security.",
  },
  {
    icon: BarChart3,
    title: "Multi-Model Prediction",
    description:
      "Uses both Logistic Regression and KNN algorithms, comparing results for more reliable predictions.",
  },
  {
    icon: PieChart,
    title: "Comprehensive Scoring",
    description:
      "Provides precision, accuracy, recall, and F1 scores for transparent and interpretable results.",
  },
];

export default function Features() {
  return (
    <section id="features" className="py-20 lg:py-28 bg-secondary">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-widest text-primary">
            Capabilities
          </p>
          <h2 className="mt-3 font-serif text-3xl font-bold tracking-tight text-foreground sm:text-4xl text-balance">
            Data-Driven Loan Assessment
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground">
            Our ML models evaluate multiple dimensions of your financial profile to
            deliver accurate loan approval predictions.
          </p>
        </div>

        <div className="mx-auto mt-16 grid max-w-5xl grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="group rounded-xl border border-border bg-card p-8 shadow-sm transition-all hover:shadow-md hover:-translate-y-0.5"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 transition-colors group-hover:bg-primary/20">
                <feature.icon className="h-6 w-6 text-primary" />
              </div>
              <h3 className="mt-5 font-serif text-lg font-semibold text-foreground">
                {feature.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
