import pandas as pd
import networkx as nx


def create_graph_from_file(file_path: str):
    df = pd.read_csv(file_path)

    G = nx.MultiDiGraph()

    for _, row in df.iterrows():
        src_ip = row['src_ip']
        dst_ip = row['dst_ip']

        G.add_edge(
            src_ip, dst_ip,
            key="flow",
            proto=row.get("proto"),
            service=row.get("service"),
            duration=row.get("duration"),
            src_bytes=row.get("src_bytes"),
            dst_bytes=row.get("dst_bytes"),
            conn_state=row.get("conn_state"),
            label=row.get("label"),
            attack_type=row.get("type")
        )

        if pd.notna(row.get("dns_query")):
            dns_domain = row["dns_query"]
            G.add_edge(
                src_ip, dns_domain,
                key="dns_query",
                qclass=row.get("dns_qclass"),
                qtype=row.get("dns_qtype"),
                rcode=row.get("dns_rcode"),
                dns_AA=row.get("dns_AA"),
                dns_RD=row.get("dns_RD"),
                dns_RA=row.get("dns_RA"),
                dns_rejected=row.get("dns_rejected")
            )

        if pd.notna(row.get("http_uri")):
            http_target = row["http_uri"]
            G.add_edge(
                src_ip, http_target,
                key="http_request",
                method=row.get("http_method"),
                version=row.get("http_version"),
                status_code=row.get("http_status_code"),
                trans_depth=row.get("http_trans_depth"),
                req_body_len=row.get("http_request_body_len"),
                resp_body_len=row.get("http_response_body_len"),
                user_agent=row.get("http_user_agent"),
                orig_mime=row.get("http_orig_mime_types"),
                resp_mime=row.get("http_resp_mime_types")
            )

        if pd.notna(row.get("ssl_subject")):
            G.add_edge(
                src_ip, row["ssl_subject"],
                key="ssl_subject",
                ssl_version=row.get("ssl_version"),
                ssl_cipher=row.get("ssl_cipher"),
                ssl_resumed=row.get("ssl_resumed"),
                ssl_established=row.get("ssl_established")
            )

        if pd.notna(row.get("ssl_issuer")):
            G.add_edge(
                src_ip, row["ssl_issuer"],
                key="ssl_issuer",
                ssl_version=row.get("ssl_version"),
                ssl_cipher=row.get("ssl_cipher"),
                ssl_resumed=row.get("ssl_resumed"),
                ssl_established=row.get("ssl_established")
            )

        if pd.notna(row.get("weird_name")):
            G.add_edge(
                src_ip, row["weird_name"],
                key="protocol_violation",
                weird_addl=row.get("weird_addl"),
                weird_notice=row.get("weird_notice")
            )

    print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    print("Edge types (views) include:", set(k for _, _, k in G.edges(keys=True)))

    return G, df
