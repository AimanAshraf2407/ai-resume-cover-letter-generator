import re
from typing import Dict, List, Set


def extract_keywords(text: str) -> Set[str]:
    """Extracts alphanumeric keywords (normalized to lowercase) excluding trivial stopwords."""
    stopwords = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
        "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
        "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
        "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i",
        "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more", "most",
        "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
        "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she",
        "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them",
        "themselves", "then", "there", "these", "they", "this", "those", "through", "to",
        "too", "under", "until", "up", "very", "was", "we", "were", "what", "when",
        "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your",
        "yours", "yourself", "yourselves"
    }
    
    words = re.findall(r"\b[a-zA-Z0-9+#.-]{2,}\b", text.lower())
    return {w for w in words if w not in stopwords}


def calculate_ats_metrics(
    candidate_profile: str,
    job_description: str,
    generated_text: str
) -> Dict[str, float]:
    """
    Computes ATS alignment metrics:
    - Precision: Fraction of keywords in generated text that came from candidate/job scope.
    - Recall / Keyword Match Rate: Fraction of target job keywords captured in the generated text.
    - F1-Score: Harmonic mean of precision and recall.
    - Hallucination Penalty: Percentage of terms completely foreign to both profile and job description.
    """
    profile_kws = extract_keywords(candidate_profile)
    job_kws = extract_keywords(job_description)
    output_kws = extract_keywords(generated_text)

    if not job_kws or not output_kws:
        return {
            "job_keyword_count": len(job_kws),
            "output_keyword_count": len(output_kws),
            "keyword_recall_pct": 0.0,
            "keyword_precision_pct": 0.0,
            "f1_score": 0.0,
        }

    # Overlaps
    matched_job_kws = output_kws.intersection(job_kws)
    valid_source_kws = profile_kws.union(job_kws)
    valid_output_kws = output_kws.intersection(valid_source_kws)

    recall = (len(matched_job_kws) / len(job_kws)) * 100
    precision = (len(valid_output_kws) / len(output_kws)) * 100 if output_kws else 0.0
    f1 = (2 * (precision * recall) / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "job_keyword_count": len(job_kws),
        "output_keyword_count": len(output_kws),
        "matched_job_keywords": len(matched_job_kws),
        "keyword_recall_pct": round(recall, 2),
        "keyword_precision_pct": round(precision, 2),
        "f1_score": round(f1, 2),
    }