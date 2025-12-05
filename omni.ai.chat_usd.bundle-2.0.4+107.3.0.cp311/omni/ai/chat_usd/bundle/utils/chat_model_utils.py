def sanitize_messages_with_expert_type(messages, expert_type, rag_max_tokens=0, rag_top_k=0):
    """
    Sanitizes messages and adds expert type metadata.
    
    Args:
        messages (list): List of message dictionaries
        expert_type (str): Type of expert to use
        rag_max_tokens (int): Maximum tokens for RAG
        rag_top_k (int): Top k results for RAG
        
    Returns:
        list: Sanitized messages with expert type metadata
    """
    if not messages:
        return messages
        
    # Add expert type to the last message
    if messages and isinstance(messages[-1], dict):
        messages[-1]["expert_type"] = expert_type
        if rag_max_tokens > 0:
            messages[-1]["rag_max_tokens"] = rag_max_tokens
        if rag_top_k > 0:
            messages[-1]["rag_top_k"] = rag_top_k
            
    return messages 