import Sidebar from "./Sidebar";

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "var(--surface-canvas)",
        color: "var(--color-ink-black)",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Sidebar />
      <main
        style={{
          flex: 1,
          padding: "40px 24px 80px 24px",
          maxWidth: "var(--page-max-width)",
          width: "100%",
          margin: "0 auto",
        }}
      >
        {children}
      </main>
    </div>
  );
}
