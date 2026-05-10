#!/usr/bin/env python3
"""
医学数据库统一搜索脚本
整合 PubMed、ClinicalTrials.gov、OpenFDA

用法:
    python3 medical_search.py pubmed "diabetic retinopathy" --max 5
    python3 medical_search.py trials "visual rehabilitation" --status RECRUITING
    python3 medical_search.py fda "metformin" --type adverse
"""

import sys
import json
import time
import ssl
import urllib.request
import urllib.parse

# 跳过 SSL 证书验证（macOS Python 3.13 兼容）
ssl._create_default_https_context = ssl._create_unverified_context

def search_pubmed(term, retmax=5):
    """搜索 PubMed 文献"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    # 第一步：搜索获取PMID
    search_url = f"{base_url}/esearch.fcgi"
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": term,
        "retmax": str(retmax),
        "retmode": "json"
    })
    
    try:
        with urllib.request.urlopen(f"{search_url}?{params}", timeout=10) as r:
            data = json.loads(r.read().decode())
            pmids = data.get("esearchresult", {}).get("idlist", [])
        
        if not pmids:
            return {"query": term, "count": 0, "papers": []}
        
        # 第二步：获取摘要
        time.sleep(0.35)  # 速率限制
        summary_url = f"{base_url}/esummary.fcgi"
        params = urllib.parse.urlencode({
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "json"
        })
        
        with urllib.request.urlopen(f"{summary_url}?{params}", timeout=15) as r:
            data = json.loads(r.read().decode())
            result = data.get("result", {})
            
            papers = []
            for pmid in pmids:
                if pmid in result and "error" not in result[pmid]:
                    item = result[pmid]
                    papers.append({
                        "pmid": pmid,
                        "title": item.get("title", ""),
                        "authors": [a.get("name", "") for a in item.get("authors", [])][:3],
                        "journal": item.get("fulljournalname", item.get("source", "")),
                        "pubdate": item.get("pubdate", ""),
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    })
            
            return {"query": term, "count": len(papers), "papers": papers}
    except Exception as e:
        return {"error": str(e)}

def search_clinical_trials(term, status="RECRUITING", pagesize=5):
    """搜索 ClinicalTrials.gov"""
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    
    params = urllib.parse.urlencode({
        "query.term": term,
        "filter.overallStatus": status,
        "pageSize": str(pagesize)
    })
    
    try:
        with urllib.request.urlopen(f"{base_url}?{params}", timeout=15) as r:
            data = json.loads(r.read().decode())
            
            trials = []
            for study in data.get("studies", []):
                proto = study.get("protocolSection", {})
                ident = proto.get("identificationModule", {})
                status_mod = proto.get("statusModule", {})
                
                trials.append({
                    "nct_id": ident.get("nctId", ""),
                    "title": ident.get("briefTitle", ""),
                    "status": status_mod.get("overallStatus", ""),
                    "start_date": status_mod.get("startDateStruct", {}).get("date", ""),
                    "url": f"https://clinicaltrials.gov/study/{ident.get('nctId', '')}"
                })
            
            return {"query": term, "status": status, "count": len(trials), "trials": trials}
    except Exception as e:
        return {"error": str(e)}

def search_openfda(drug_name, search_type="adverse", limit=5):
    """搜索 OpenFDA（默认limit=5，避免大结果集超时）"""
    if search_type == "adverse":
        url = "https://api.fda.gov/drug/event.json"
        search_field = f'patient.drug.medicinalproduct:"{drug_name}"'
    elif search_type == "label":
        url = "https://api.fda.gov/drug/label.json"
        search_field = f'openfda.brand_name:"{drug_name}"'
    else:
        url = "https://api.fda.gov/drug/enforcement.json"
        search_field = f'product_description:"{drug_name}"'
    
    params = urllib.parse.urlencode({
        "search": search_field,
        "limit": str(limit)
    })
    
    try:
        with urllib.request.urlopen(f"{url}?{params}", timeout=15) as r:
            raw = r.read().decode()
            # 截断过大响应，只解析前limit条
            data = json.loads(raw)
            
            results = []
            for item in data.get("results", [])[:limit]:
                if search_type == "adverse":
                    patient = item.get("patient", {})
                    results.append({
                        "case_number": item.get("safetyreportid", item.get("case_number", "")),
                        "event_date": item.get("receiptdate", item.get("event_date", "")),
                        "serious": str(item.get("serious", "")),
                        "drugs": [d.get("medicinalproduct", "") for d in patient.get("drug", [])][:3]
                    })
                elif search_type == "label":
                    results.append({
                        "brand_name": item.get("openfda", {}).get("brand_name", [""])[0],
                        "generic_name": item.get("openfda", {}).get("generic_name", [""])[0],
                        "manufacturer": item.get("openfda", {}).get("manufacturer_name", [""])[0]
                    })
                else:
                    results.append({
                        "product_description": item.get("product_description", ""),
                        "recall_date": item.get("recall_initiation_date", ""),
                        "reason": item.get("reason_for_recall", "")
                    })
            
            total = data.get("meta", {}).get("results", {}).get("total", "?")
            return {"query": drug_name, "type": search_type, "total_available": total, "returned": len(results), "results": results}
    except Exception as e:
        return {"query": drug_name, "type": search_type, "error": str(e)}

def main():
    if len(sys.argv) < 3:
        print("用法: python3 medical_search.py <source> <query> [options]")
        print("  source: pubmed | trials | fda")
        print("  pubmed: --max N")
        print("  trials: --status RECRUITING|COMPLETED")
        print("  fda: --type adverse|label|recall")
        sys.exit(1)
    
    source = sys.argv[1].lower()
    query = sys.argv[2]
    
    if source == "pubmed":
        retmax = 5
        for i, arg in enumerate(sys.argv):
            if arg == "--max" and i + 1 < len(sys.argv):
                retmax = int(sys.argv[i + 1])
        result = search_pubmed(query, retmax)
    
    elif source == "trials":
        status = "RECRUITING"
        for i, arg in enumerate(sys.argv):
            if arg == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
        result = search_clinical_trials(query, status)
    
    elif source == "fda":
        search_type = "adverse"
        for i, arg in enumerate(sys.argv):
            if arg == "--type" and i + 1 < len(sys.argv):
                search_type = sys.argv[i + 1]
        result = search_openfda(query, search_type)
    
    else:
        print(f"未知数据源: {source}")
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
