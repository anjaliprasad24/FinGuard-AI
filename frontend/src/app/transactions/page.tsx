"use client";

import { useEffect, useState } from "react";
import { Transaction } from "@/lib/types";
import { api } from "@/lib/api";
import TransactionFeed from "@/components/TransactionFeed";
import { Upload, Plus, FileText, CheckCircle } from "lucide-react";

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categoryFilter, setCategoryFilter] = useState("ALL");
  const [showOCRModal, setShowOCRModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [ocrResult, setOcrResult] = useState<any>(null);

  const loadTxns = async () => {
    try {
      const data = await api.getTransactions(categoryFilter === "ALL" ? undefined : categoryFilter);
      setTransactions(data);
    } catch (e) {}
  };

  useEffect(() => {
    loadTxns();
  }, [categoryFilter]);

  const handleOCRUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;
    setUploading(true);
    try {
      const res = await api.uploadOCR(selectedFile);
      setOcrResult(res.extracted_data);
      // Automatically ingest extracted transaction
      const ext = res.extracted_data;
      const ingestRes = await api.ingestTransaction({
        raw_merchant: ext.raw_text || ext.merchant,
        amount: ext.amount,
        category: ext.category,
      });
      setTransactions((prev) => [ingestRes.transaction, ...prev]);
    } catch (err) {
      alert("OCR Upload Failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Transactions & Receipt OCR</h1>
          <p className="text-xs text-slate-400">Ingest, Scrub PII, and Audit Categorized Financial Stream</p>
        </div>
        <button
          onClick={() => setShowOCRModal(true)}
          className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-4 py-2.5 rounded-lg shadow-lg shadow-blue-500/20 flex items-center space-x-2 text-sm transition"
        >
          <Upload className="w-4 h-4" />
          <span>Upload Receipt OCR</span>
        </button>
      </div>

      <div className="flex items-center space-x-2 overflow-x-auto pb-2">
        {["ALL", "Electronics", "Dining & Food", "Groceries", "Utilities & Bills", "Travel & Transport"].map((cat) => (
          <button
            key={cat}
            onClick={() => setCategoryFilter(cat)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              categoryFilter === cat
                ? "bg-blue-600 text-white shadow"
                : "bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      <TransactionFeed transactions={transactions} />

      {/* OCR Modal */}
      {showOCRModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-full max-w-md shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-1">Upload Receipt / Invoice Image</h3>
            <p className="text-xs text-slate-400 mb-4">Tesseract Engine extracts merchant, amount & line items after scrubbing PII</p>

            <form onSubmit={handleOCRUpload} className="space-y-4">
              <div className="border-2 border-dashed border-slate-700 hover:border-blue-500 rounded-xl p-6 text-center cursor-pointer transition">
                <input
                  type="file"
                  accept="image/*,.pdf"
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  className="hidden"
                  id="ocr-file-input"
                />
                <label htmlFor="ocr-file-input" className="cursor-pointer">
                  <FileText className="w-8 h-8 text-blue-400 mx-auto mb-2" />
                  <span className="text-sm font-medium text-slate-200 block">
                    {selectedFile ? selectedFile.name : "Click to select Receipt PNG, JPG or PDF"}
                  </span>
                  <span className="text-xs text-slate-500 block mt-1">Files up to 10MB</span>
                </label>
              </div>

              {ocrResult && (
                <div className="bg-slate-950 p-3 rounded-lg border border-emerald-500/30 text-xs text-emerald-300">
                  <div className="flex items-center space-x-1.5 font-bold mb-1">
                    <CheckCircle className="w-4 h-4 text-emerald-400" />
                    <span>OCR Ingestion Complete</span>
                  </div>
                  <div>Merchant: {ocrResult.merchant}</div>
                  <div>Extracted Amount: ₹{ocrResult.amount}</div>
                  <div>Category: {ocrResult.category}</div>
                </div>
              )}

              <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => {
                    setShowOCRModal(false);
                    setOcrResult(null);
                  }}
                  className="px-4 py-2 rounded-lg text-sm text-slate-400 hover:text-white"
                >
                  Close
                </button>
                <button
                  type="submit"
                  disabled={uploading || !selectedFile}
                  className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-semibold px-4 py-2 rounded-lg text-sm transition"
                >
                  {uploading ? "Extracting OCR..." : "Extract & Process"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
